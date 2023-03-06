import csv
from core.choices import STATUS_CHOICES
from csvGenerator import settings
from faker import Faker
from csvGenerator.celery import app
from core.models import Schema, DataSet, Column


@app.task
def generate_data_task(dataset_id):
    fake = Faker()
    dataset = DataSet.objects.filter(id=dataset_id).first()
    if not dataset:
        return
    schema = Schema.objects.filter(id=dataset.schema_id).first()
    columns = Column.objects.filter(schema=schema.id).order_by("order").values()
    separator = schema.column_separator
    quote = schema.string_character
    row_number = dataset.rows
    header = []
    all_rows = []
    url = ''
    for column in columns:
        header.append(column["title"])
    for row in range(row_number):
        raw_row = []
        for column in columns:
            column_type = column["type"]
            if column_type == 0:
                data = fake.name()
            elif column_type == 1:
                data = fake.job()
            elif column_type == 2:
                data = fake.email()
            elif column_type == 3:
                data = fake.domain_name()
            elif column_type == 4:
                data = fake.phone_number()
            elif column_type == 5:
                data = fake.company()
            elif column_type == 6:
                data = fake.sentences(
                    nb=fake.random_int(
                        min=column["range_from"] or 1,
                        max=column["range_to"] or 10
                    )
                )
                data = " ".join(data)

            elif column_type == 7:
                data = fake.random_int(
                    min=column["range_from"] or 0,
                    max=column["range_to"] or 99999
                )
            elif column_type == 8:
                data = fake.address()
            elif column_type == 9:
                data = fake.date()
            else:
                data = None
            raw_row.append(data)
        all_rows.append(raw_row)
        url = f'{settings.MEDIA_ROOT}/dataset-{dataset.id}.csv'
        with open(url, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=separator, quotechar=quote, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            writer.writerows(all_rows)

            dataset.status = STATUS_CHOICES[1][1]
            dataset.save()
    dataset.download_link = url
    dataset.save()