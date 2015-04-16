from django.shortcuts import render
from django.views import generic

from statscollect_db import models


class IndexView(generic.ListView):
    template_name = 'statscollect_scrap/index.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        """Return the list of all tournaments"""
        return models.Tournament.objects.all()


class TournamentDetailView(generic.ListView):
    template_name = 'statscollect_scrap/tournament_detail.html'
    context_object_name = 'instance_list'

    def get_queryset(self):
        """Return the list of instances of the tournament"""
        pk = self.kwargs.get('pk')
        return models.TournamentInstance.objects.filter(tournament_id=pk).order_by('name')


class InstanceDetailView(generic.ListView):
    template_name = 'statscollect_scrap/instance_detail.html'
    context_object_name = 'step_list'

    def get_queryset(self):
        """Return the list of steps of the instance"""
        pk = self.kwargs.get('pk')
        return models.TournamentInstanceStep.objects.filter(tournament_instance_id=pk).order_by('name')