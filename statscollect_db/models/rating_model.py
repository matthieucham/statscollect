import uuid
from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone

from .meeting_model import Meeting
from .person_model import Person


class RatingSource(models.Model):
    FIELD_CHOICES = (
        ('FOOTBALL', 'Football'),
    )
    TYPE_CHOICES = (
        ('10CLASSIC', 'Classical 0-10'),
        ('6GERMAN', 'German 1-6'),
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)
    code = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=400, blank=True)
    field = models.CharField(max_length=10, choices=FIELD_CHOICES, blank=True)
    country = CountryField(blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default='10CLASSIC')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.code:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(RatingSource, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'source de notes'
        verbose_name_plural = 'sources de notes'


class Rating(models.Model):
    person = models.ForeignKey(Person)
    meeting = models.ForeignKey(Meeting)
    source = models.ForeignKey(RatingSource)
    original_rating = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        self.meeting.save()

    class Meta:
        verbose_name = 'note'