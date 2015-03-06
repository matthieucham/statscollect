from django.db import models
from django_countries.fields import CountryField

from .meta_model import MetaModel


class Tournament(MetaModel):
    FIELD_CHOICES = (
        ('FOOTBALL', 'Football'),
    )
    TYPE_CHOICES = (
        ('NAT', 'National'),
        ('INT', 'International'),
    )
    name = models.CharField(max_length=50)
    field = models.CharField(max_length=10, choices=FIELD_CHOICES, blank=False)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, blank=False)
    country = CountryField(blank=True)

    def __str__(self):
        return self.name


class TournamentInstance(MetaModel):
    STATUS_CHOICES = (
        ('ONGOING', 'Ongoing'),
        ('ARCHIVED', 'Archived'),
    )
    tournament = models.ForeignKey(Tournament)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, blank=False, default='ARCHIVED')

    def __str__(self):
        return self.name


class TournamentInstanceStep(MetaModel):
    tournament_instance = models.ForeignKey(TournamentInstance, related_name='steps')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
