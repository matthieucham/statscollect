from django.db import models

from .meta_model import MetaModel

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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class FootballPerson(Person):
    POSITION_CHOICES = (
        ('G', 'Goalkeeper'),
        ('D', 'Defender'),
        ('M', 'Midfielder'),
        ('A', 'Striker'),
    )
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)