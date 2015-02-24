from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters

from statscollect_db import models
from statscollect_db import serializers


class FootballMeetingViewSet(viewsets.ModelViewSet):
    queryset = models.FootballMeeting.objects.all()
    serializer_class = serializers.FootballMeetingDetailedSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
