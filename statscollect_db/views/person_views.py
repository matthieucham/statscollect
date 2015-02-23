from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters

from statscollect_db.models import Person
from statscollect_db.serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (
        filters.SearchFilter,
        filters.DjangoFilterBackend
    )
    search_fields = (
        'last_name',
        'usual_name',
    )
    filter_fields = (
        'uuid',
        'field',
        'status',
    )