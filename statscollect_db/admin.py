from django.contrib import admin
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget

from statscollect_db.models import Person
from statscollect_db.models.tournament_model import Tournament, TournamentInstance, \
    TournamentInstanceStep
from statscollect_db.models.team_model import Team
from statscollect_db.models.rating_model import RatingSource, Rating
from statscollect_db.models.meeting_model import TeamMeeting
from statscollect_db.models.football_stats_model import FootballPersonalStats

# Register your models here.
admin.site.register(Person)
admin.site.register(RatingSource)
admin.site.register(TeamMeeting)
admin.site.register(FootballPersonalStats)
admin.site.register(Rating)


class InstanceInline(admin.StackedInline):
    model = TournamentInstance
    extra = 1


class StepInline(admin.TabularInline):
    model = TournamentInstanceStep
    extra = 10


class InstanceAdmin(admin.ModelAdmin):
    inlines = [StepInline]


class TournamentAdmin(admin.ModelAdmin):
    inlines = [InstanceInline]
    list_display = ('name', 'field', 'type')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentInstance, InstanceAdmin)


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'short_name', 'field', 'current_members', 'country',)
        widget = {'country': CountrySelectWidget}


class TeamAdmin(admin.ModelAdmin):
    model = Team
    filter_horizontal = ('current_members',)
    form = TeamForm


admin.site.register(Team, TeamAdmin)