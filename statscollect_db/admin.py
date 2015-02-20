from django.contrib import admin
from merged_inlines.admin import MergedInlineAdmin

from statscollect_db.forms import FootballPersonForm, FootballTeamForm,FootballMeetingForm

from statscollect_db.models import FootballPerson
from statscollect_db.models.tournament_model import Tournament, TournamentInstance, \
    TournamentInstanceStep
from statscollect_db.models.team_model import FootballTeam
from statscollect_db.models.rating_model import RatingSource, Rating
from statscollect_db.models.meeting_model import FootballMeeting
from statscollect_db.models.football_stats_model import FootballPersonalStats


class InstanceInline(admin.StackedInline):
    model = TournamentInstance
    extra = 1


class StepInline(admin.TabularInline):
    model = TournamentInstanceStep
    extra = 10


class InstanceAdmin(admin.ModelAdmin):
    inlines = [StepInline]
    list_display = ('name', 'get_tournament', 'get_field')

    def get_tournament(self, obj):
        return obj.tournament.name

    get_tournament.short_description = 'Tournament'
    get_tournament.admin_order_field = 'tournament__name'

    def get_field(self, obj):
        return obj.tournament.field

    get_field.short_description = 'Field'
    get_field.admin_order_field = 'tournament__field'


class TournamentAdmin(admin.ModelAdmin):
    inlines = [InstanceInline]
    list_display = ('name', 'field', 'type')


class FootballTeamAdmin(admin.ModelAdmin):
    model = FootballTeam
    filter_horizontal = ('current_members',)
    form = FootballTeamForm

    def get_queryset(self, request):
        return FootballTeam.objects.filter(field__contains='FOOTBALL')


class FootballPersonAdmin(admin.ModelAdmin):
    form = FootballPersonForm
    fieldsets = (
        ('Identity', {'fields': ('last_name', 'first_name', 'usual_name', 'birth', 'sex', 'rep_country')}),
        ('Status', {'fields': ('status', 'current_teams')}),
    )

    def get_queryset(self, request):
        return FootballPerson.objects.filter(field__contains='FOOTBALL')


class FootballStatsInline(admin.TabularInline):
    model = FootballPersonalStats
    extra = 28


class RatingsInline(admin.StackedInline):
    model = Rating
    extra = 28


class FootballMeetingAdmin(admin.ModelAdmin):
    #merged_inline_order = 'person_id'
    inlines = [FootballStatsInline, RatingsInline]
    form = FootballMeetingForm

# Register your models here.
admin.site.register(RatingSource)
admin.site.register(Rating)
admin.site.register(FootballMeeting, FootballMeetingAdmin)
admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(FootballPerson, FootballPersonAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentInstance, InstanceAdmin)