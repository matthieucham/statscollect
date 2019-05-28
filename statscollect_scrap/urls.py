from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^datasheets/(?P<hash_url>[a-f0-9]{8,})/$',
        views.scraped_datasheet_detail),
    url(r'^teams/(?P<team_name>[a-zA-Z\s-]{3,})/$',
        views.scraped_team_with_players),
]