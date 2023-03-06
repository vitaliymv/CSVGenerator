import os.path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.edit import FormMixin
from core.tasks import generate_data_task
from core.choices import STATUS_CHOICES
from core.forms import DataSetForm
from core.models import Schema, Column, DataSet
from csvGenerator.settings import MEDIA_ROOT

column_formset = inlineformset_factory(
    Schema, Column, fields=('title', 'type', 'order', 'range_from', 'range_to'),
    labels={'title': 'Column name', 'type': 'Type',
            'order': 'Order', 'range_from': 'From', 'range_to': 'To'},
    can_order=False, can_delete=True, extra=0
)


# Create your views here.
class SchemasView(LoginRequiredMixin, ListView):
    template_name = "schemas.html"
    model = Schema

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class CreateSchemaView(LoginRequiredMixin, CreateView):
    model = Schema
    fields = ['title', 'column_separator', 'string_character']
    success_url = "/schemas"
    template_name = "new-schema.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["columns"] = column_formset(self.request.POST)
        else:
            context["columns"] = column_formset()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        columns = context["columns"]
        if not columns.is_valid():
            return super().form_invalid(form)
        self.object = form.save()
        columns.instance = self.object
        columns.save()
        return super().form_valid(form)


class UpdateSchemaView(LoginRequiredMixin, UpdateView):
    model = Schema
    fields = ['title', 'column_separator', 'string_character']
    success_url = "/schemas"
    template_name = "new-schema.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["columns"] = column_formset(self.request.POST, instance=self.object)
        else:
            context["columns"] = column_formset(instance=self.object)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        columns = context["columns"]
        if not columns.is_valid():
            return super().form_invalid(form)
        self.object = form.save()
        columns.instance = self.object
        columns.save()
        return super().form_valid(form)


class DeleteSchemaView(LoginRequiredMixin, DeleteView):
    template_name = "confirm_delete.html"
    model = Schema
    success_url = "/schemas"


class DataSetView(LoginRequiredMixin, FormMixin, ListView):
    model = DataSet
    form_class = DataSetForm
    template_name = "datasets.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(schema_id=self.schema_id)

    def form_valid(self, form):
        form.instance.schema_id = self.schema_id
        form.instance.status = STATUS_CHOICES[0][1]

        dataset = form.save()

        generate_data_task.delay(dataset.id)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        self.schema_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.path


class DownloadCsvView(TemplateView):
    template_name = "datasets.html"

    def get(self, request, *args, **kwargs):
        filepath = os.path.join(MEDIA_ROOT, f"dataset-{kwargs.get('pk_ds')}.csv")
        try:
            with open(filepath, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/CSV")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                return response
        except:
            raise Http404
