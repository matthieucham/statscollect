from django.db import models
from django.utils import timezone
from django_extensions.db.fields import UUIDField


class MetaModel(models.Model):
    uuid = UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

