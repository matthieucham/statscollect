from django.db import models
from django.utils import timezone
from django_extensions.db.fields import UUIDField


class MetaModel(models.Model):
    uuid = UUIDField(unique=True)

    class Meta:
        abstract = True

