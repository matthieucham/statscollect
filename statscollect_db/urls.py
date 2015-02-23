from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from statscollect_db import views
from statscollect_db.views.apiroot_view import api_root

ratingsource_list = views.RatingSourceViewSet.as_view({
    'get': 'list'
})
ratingsource_detail = views.RatingSourceViewSet.as_view({
    'get': 'retrieve'
})
footballteam_list = views.FootballTeamViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
footballteam_detail = views.FootballTeamViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
person_list = views.PersonViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

person_detail = views.PersonViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

person_urls = patterns(
    '',
    url(r'^/$',
        person_list,
        name='person-list'),
    url(r'^/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        person_detail,
        name='person-detail'),
    url(
        r'^/(?P<person>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/current_teams$',
        views.FootballTeamViewSet.as_view({'get': 'list', }, suffix='List'),
        name='person-currentteam-list-nested'),
)

tournament_urls = patterns(
    '',
    url(r'^/$',
        views.TournamentViewSet.as_view({'get': 'list', }, suffix='List'),
        name='tournament-list'),
    url(r'^/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.TournamentViewSet.as_view({'get': 'retrieve', }),
        name='tournament-detail'),
    url(r'^/(?P<tournament>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/instances$',
        views.TournamentInstanceViewSet.as_view({'get': 'list', }, suffix='List'),
        name='tournament-instance-list-nested'),
)

tournament_instance_urls = patterns(
    '',
    url(r'^/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.TournamentInstanceViewSet.as_view({'get': 'retrieve', }),
        name='instance-detail'),
)

urlpatterns = [
    url(r'^$', api_root),
    url(r'^rating_sources/$', ratingsource_list, name='ratingsource-list'),
    url(r'^rating_sources/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        ratingsource_detail, name='ratingsource-detail'),
    url(r'^football_teams/$', footballteam_list, name='footballteam-list'),
    url(r'^football_teams/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        footballteam_detail, name='footballteam-detail'),
    url(r'^persons', include(person_urls)),
    url(r'^tournaments', include(tournament_urls)),
    url(r'^tournament_instances', include(tournament_instance_urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)