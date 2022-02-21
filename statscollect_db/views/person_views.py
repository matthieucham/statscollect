from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from statscollect_db.models import Person, FootballPerson
from statscollect_db.serializers import PersonSerializer, FootballPlayerSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "uuid"
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = (
        "last_name",
        "usual_name",
    )
    filter_fields = (
        "uuid",
        "field",
        "status",
    )


class FootballPlayerViewSet(PersonViewSet):
    queryset = FootballPerson.objects.all()
    serializer_class = FootballPlayerSerializer
