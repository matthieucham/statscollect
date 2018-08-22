from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from statscollect_db import views
from statscollect_db.views.apiroot_view import api_root


ratingsource_list = views.RatingSourceViewSet.as_view({'get': 'list'}, suffix='List')
ratingsource_detail = views.RatingSourceViewSet.as_view({
    'get': 'retrieve'
})
footballteam_list = views.FootballTeamViewSet.as_view({'get': 'list'}, suffix='List')
footballteam_detail = views.FootballTeamViewSet.as_view({
    'get': 'retrieve',
})
footballplayer_list = views.FootballPlayerViewSet.as_view({'get': 'list'}, suffix='List')

footballplayer_detail = views.FootballPlayerViewSet.as_view({
    'get': 'retrieve',
})

person_urls = [
    url(r'^(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.PersonViewSet.as_view({
            'get': 'retrieve',
        }),
        name='person_detail')]

footballplayer_urls = [
    url(r'^$',
        footballplayer_list,
        name='footballplayer-list'),
    url(r'^(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        footballplayer_detail,
        name='footballplayer-detail'),
    url(
        r'^(?P<person>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/current_teams$',
        views.FootballTeamViewSet.as_view({'get': 'list', }, suffix='List'),
        name='footballplayer-currentteam-list-nested'),

    url(
        r'^(?P<person>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/meetings',
        views.PlayerMeetingHistoryViewSet.as_view({'get': 'list', }, suffix='List'),
        name='footballplayer-instance-list-nested'),

    url(
        r'^(?P<person>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/instances/(?P<instance>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/meetings$',
        views.FootballMeetingSummaryViewSet.as_view({'get': 'list', }, suffix='List'),
        name='footballplayer-meetings-list-nested')]

tournament_urls = [
    url(r'^$',
        views.TournamentViewSet.as_view({'get': 'list', }, suffix='List'),
        name='tournament-list'),
    url(r'^(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.TournamentViewSet.as_view({'get': 'retrieve', }),
        name='tournament-detail'),
    url(r'^(?P<tournament>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/instances$',
        views.TournamentInstanceViewSet.as_view({'get': 'list', }, suffix='List'),
        name='tournament-instance-list-nested')]

tournament_instance_urls = [
    url(r'^(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.TournamentInstanceViewSet.as_view({'get': 'retrieve', }),
        name='instance-detail')]

tournament_instance_step_urls = [
    url(r'^(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.TournamentInstanceStepViewSet.as_view({'get': 'retrieve', }),
        name='step-detail'),
]

footballmeeting_urls = [
    url(r'^(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.FootballMeetingViewSet.as_view({'get': 'retrieve', }),
        name='footballmeeting-detail')]

urlpatterns = [
    url(r'^$', api_root),
    url(r'^rating_sources/$', ratingsource_list, name='ratingsource-list'),
    url(r'^football_teams/$', footballteam_list, name='footballteam-list'),
    url(r'^football_teams/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        footballteam_detail, name='footballteam-detail'),
    url(r'^football_players/', include(footballplayer_urls)),
    url(r'^tournaments/', include(tournament_urls)),
    url(r'^tournament_instances/', include(tournament_instance_urls)),
    url(r'^steps/', include(tournament_instance_step_urls)),
    url(r'^footballmeetings/', include(footballmeeting_urls)),
    url(r'^persons/', include(person_urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)