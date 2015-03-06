from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters

from statscollect_db import models
from statscollect_db import serializers


class FootballMeetingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FootballMeetingDetailedSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return models.FootballMeeting.objects.all().order_by('date')


class FootballMeetingSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FootballMeetingSummarySerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        person = self.kwargs.get('person')
        instance = self.kwargs.get('instance')
        if (person is not None) and (instance is not None):
            queryset = models.FootballMeeting.objects.filter(tournament_instance__uuid=instance).filter(
                participants__uuid__contains=person).order_by('date')
            return queryset
        return models.FootballMeeting.objects.all().order_by('date')


class PlayerMeetingHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FootballMeetingSummarySerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        person = self.kwargs.get('person')
        if person is not None:
            #player = FootballPerson.objects.get(uuid=person)
            # try:
            #     meetings = player.teammeeting_set
            #     queryset = TournamentInstance.objects.filter(
            #         meetings__in=meetings.all())
            #     return queryset
            # except ObjectDoesNotExist:
            #     pass
            queryset = models.FootballMeeting.objects.filter(participants__uuid__exact=person).order_by('date')
            return queryset
        return models.FootballMeeting.objects.all()