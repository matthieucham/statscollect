from django.db import models
from django_countries.fields import CountryField

from .meta_model import MetaModel
from .meeting_model import Meeting
from .person_model import Person


class RatingSource(MetaModel):
    FIELD_CHOICES = (
        ('FOOTBALL', 'Football'),
    )
    TYPE_CHOICES = (
        ('10CLASSIC', 'Classical 0-10'),
        ('6GERMAN', 'German 1-6'),
    )
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=400)
    code = models.CharField(max_length=8)
    field = models.CharField(max_length=10, choices=FIELD_CHOICES, blank=True)
    country = CountryField(blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default='10CLASSIC')

    def __str__(self):
        return self.name


class Rating(models.Model):
    person = models.ForeignKey(Person)
    meeting = models.ForeignKey(Meeting)
    source = models.ForeignKey(RatingSource)
    original_rating = models.DecimalField(null=True, max_digits=5, decimal_places=2)