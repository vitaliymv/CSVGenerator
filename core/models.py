from django.contrib.auth.models import User
from django.db import models
from core.choices import *


# Create your models here.
class Schema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    column_separator = models.CharField(max_length=5, choices=SEPARATOR_CHOICES, default=",")
    string_character = models.CharField(max_length=5, choices=CHAR_CHOICES, default='"')

    def __str__(self):
        return f"{self.user.username} -> {self.title}"


class Column(models.Model):
    schema = models.ForeignKey('Schema', on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    type = models.IntegerField(choices=DATA_TYPES_CHOICES)
    order = models.IntegerField(blank=True, default=0)
    range_from = models.IntegerField(blank=True, null=True)
    range_to = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.schema} -> {self.title}"


class DataSet(models.Model):
    schema = models.ForeignKey('Schema', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    rows = models.IntegerField(null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    download_link = models.URLField()

    def __str__(self):
        return f"{self.schema} -> {self.status}"
