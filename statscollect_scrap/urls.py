from django.conf.urls import url

from statscollect_scrap import views

urlpatterns = [
    # ex: /scrap/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /scrap/tournament/5/
    url(r'^tournament/(?P<pk>\d+)/$', views.TournamentDetailView.as_view(), name='tournament_detail'),
    # ex: /scrap/instance/1/
    url(r'^instance/(?P<pk>\d+)/$', views.InstanceDetailView.as_view(),
        name='instance_detail')]