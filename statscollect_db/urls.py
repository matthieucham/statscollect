from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from statscollect_db import views
from statscollect_db.views import FootballTeamViewSet, RatingSourceViewSet, PersonViewSet,TournamentViewSet

ratingsource_list = RatingSourceViewSet.as_view({
    'get': 'list'
})
ratingsource_detail = RatingSourceViewSet.as_view({
    'get': 'retrieve'
})
footballteam_list = FootballTeamViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
footballteam_detail = FootballTeamViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
person_list = PersonViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

person_detail = PersonViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

person_urls = patterns(
    '',
    url(r'^/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        person_detail,
        name='person-detail'),
    url(
        r'^/(?P<person>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/current_teams$',
        FootballTeamViewSet.as_view({'get': 'list', }, suffix='List'),
        name='person-currentteam-list-nested'),
)

tournament_urls = patterns(
    '',
    url(r'^/$',
        TournamentViewSet.as_view({'get': 'list', }, suffix='List'),
        name='tournament-list'),
    url(r'^/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        TournamentViewSet.as_view({'get': 'retrieve', }),
        name='tournament-detail'),
)

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^rating_sources/$', ratingsource_list, name='ratingsource-list'),
    url(r'^rating_sources/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        ratingsource_detail, name='ratingsource-detail'),
    url(r'^football_teams/$', footballteam_list, name='footballteam-list'),
    url(r'^football_teams/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        footballteam_detail, name='footballteam-detail'),
    url(r'^persons', include(person_urls)),
    url(r'^tournaments', include(tournament_urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)