from django.db import models, transaction
from django.apps import apps


class FootballTeamManager(models.Manager):
    def get_queryset(self):
        return super(FootballTeamManager, self).get_queryset().filter(field='FOOTBALL')


class PersonManager(models.Manager):

    def order_by_meeting_count(self, person_1, person_2):
        teammeetingperson_model = apps.get_model('statscollect_db', 'TeamMeetingPerson')
        count_1 = teammeetingperson_model.objects.filter(person=person_1).count()
        count_2 = teammeetingperson_model.objects.filter(person=person_2).count()
        if count_1 <= count_2:
            return person_1, person_2
        else:
            return person_2, person_1

    @transaction.atomic
    def merge(self, source, target, delete_source=False):
        rating_model = apps.get_model('statscollect_db', 'Rating')
        teammeetingperson_model = apps.get_model('statscollect_db', 'TeamMeetingPerson')
        rating_model.objects.filter(person=source).select_for_update().update(person=target)
        teammeetingperson_model.objects.filter(person=source).select_for_update().update(person=target)


class FootballPersonManager(PersonManager):
    def get_queryset(self):
        return super(FootballPersonManager, self).get_queryset().filter(field='FOOTBALL')

    @transaction.atomic
    def merge(self, source, target, delete_source=False):
        super(FootballPersonManager, self).merge(source, target, delete_source=delete_source)
        stats_model = apps.get_model('statscollect_db', 'FootballPersonalStats')
        stats_model.objects.filter(person=source).select_for_update().update(person=target)
