from django.db import models

from .meta_model import MetaModel
from .person_model import Person
from .managers import FootballTeamManager

from django_countries.fields import CountryField


class Team(MetaModel):
    FIELD_CHOICES = (
        ('FOOTBALL', 'Football'),
        ('CYCLING', 'Cycling'),
    )
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    field = models.CharField(max_length=10, choices=FIELD_CHOICES)
    country = CountryField(blank=True)
    current_members = models.ManyToManyField(Person, related_name='current_teams', blank=True)
    migration_id = models.CharField(max_length=35, unique=True, null=True)
    # TODO : restreindre aux personnes de même field dans le formulaire.

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-country', 'name']


class FootballTeam(Team):
    class Meta:
        proxy = True
        verbose_name = 'club (football)'
        verbose_name_plural = 'clubs (football)'

    objects = FootballTeamManager()

    def save(self, *args, **kwargs):
        self.field = 'FOOTBALL'
        super(FootballTeam, self).save(*args, **kwargs)