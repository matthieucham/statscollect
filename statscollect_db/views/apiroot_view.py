from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'rating_sources': reverse('ratingsource-list', request=request, format=format),
        'football_teams': reverse('footballteam-list', request=request, format=format),
        'tournaments': reverse('tournament-list', request=request, format=format),
    })