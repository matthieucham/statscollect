from django.db import models
from django.utils import timezone
from django_extensions.db.fields import UUIDField


class MetaModel(models.Model):
    uuid = UUIDField(unique=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(MetaModel, self).save(*args, **kwargs)

