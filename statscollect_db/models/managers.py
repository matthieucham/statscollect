from django.db import models


class FootballTeamManager(models.Manager):
    def get_queryset(self):
        return super(FootballTeamManager, self).get_queryset().filter(field='FOOTBALL')


class FootballPersonManager(models.Manager):
    def get_queryset(self):
        return super(FootballPersonManager, self).get_queryset().filter(field='FOOTBALL')
