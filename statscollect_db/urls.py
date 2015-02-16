from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from statscollect_db import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rating_sources/$', views.rating_source_list),
    url(r'^rating_sources/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        views.rating_source_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)