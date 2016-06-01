from django.db import models

from .meta_model import MetaModel
from .managers import FootballPersonManager

from django_countries.fields import CountryField


class Person(MetaModel):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    FIELD_CHOICES = (
        ('FOOTBALL', 'Football'),
    )
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'),
    )
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    usual_name = models.CharField(max_length=50, blank=True)
    birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')
    rep_country = CountryField(blank=True)
    field = models.CharField(max_length=10, choices=FIELD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    migration_id = models.CharField(max_length=35, unique=True, null=True)

    def __str__(self):
        if self.usual_name:
            return "%s (%s %s)" % (self.usual_name, self.first_name, self.last_name)
        else:
            return "%s %s" % (self.first_name, self.last_name)


class FootballPerson(Person):
    class Meta:
        proxy = True
        verbose_name = 'footballeur'
        ordering = ['last_name', 'usual_name', 'first_name']

    objects = FootballPersonManager()

    def save(self, *args, **kwargs):
        self.field = 'FOOTBALL'
        super(FootballPerson, self).save(*args, **kwargs)