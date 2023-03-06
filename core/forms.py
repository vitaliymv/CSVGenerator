from django.forms import ModelForm
from core.models import DataSet


class DataSetForm(ModelForm):
    class Meta:
        model = DataSet
        fields = ['rows']

