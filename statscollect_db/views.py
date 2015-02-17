from django.http import HttpResponse
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import viewsets

from statscollect_db.models import RatingSource, Team
from statscollect_db.serializers import RatingSourceSerializer, FootballTeamSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'rating_sources': reverse('ratingsource-list', request=request, format=format),
        'football_teams': reverse('footballteam-list', request=request, format=format),
    })


class RatingSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RatingSource.objects.all()
    serializer_class = RatingSourceSerializer
    lookup_field = 'uuid'


class FootballTeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.filter(field__exact='FOOTBALL')
    serializer_class = FootballTeamSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)