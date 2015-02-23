from rest_framework import permissions
from rest_framework import viewsets

from statscollect_db.models import FootballTeam
from statscollect_db.serializers import FootballTeamSerializer


class FootballTeamViewSet(viewsets.ModelViewSet):
    serializer_class = FootballTeamSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        person = self.kwargs.get('person', None)
        if person is not None:
            queryset = FootballTeam.objects.filter(
                current_members__uuid__contains=person
            )
            return queryset
        queryset = FootballTeam.objects.all()
        return queryset