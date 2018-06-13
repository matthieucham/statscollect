from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from functools import partial

from statscollect_db.forms import FootballPersonForm, FootballTeamForm, FootballMeetingForm, \
    FootballTeamMeetingPersonInlineForm

from statscollect_db.models import FootballPerson, Person
from statscollect_db.models.tournament_model import Tournament, TournamentInstance, \
    TournamentInstanceStep
from statscollect_db.models.team_model import FootballTeam
from statscollect_db.models.rating_model import RatingSource, Rating
from statscollect_db.models.meeting_model import FootballMeeting, TeamMeetingPerson
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
    readonly_fields = ('uuid',)
    list_display = (
        'uuid',
        'name',
    )
    fields = ('uuid', 'name', 'short_name', 'current_members', 'country',)

    def get_queryset(self, request):
        return FootballTeam.objects.filter(field__contains='FOOTBALL')


class FootballPersonAdmin(admin.ModelAdmin):
    form = FootballPersonForm
    fieldsets = (
        ('Identity', {'fields': ('uuid', 'last_name', 'first_name', 'usual_name', 'native_name',
                                 'birth', 'sex', 'rep_country',
                                 'position')}),
        ('Status', {'fields': ('status', 'current_teams')}),
    )
    search_fields = ['last_name', 'usual_name', 'uuid']
    readonly_fields = ('uuid',)
    list_display = (
        'uuid',
        'first_name',
        'last_name',
        'usual_name',
        'position',
        'updated_at',
    )
    ordering = ('-updated_at',)
    actions = ['merge_players_action', ]

    def merge_players_action(self, request, queryset):
        try:
            assert queryset.count() == 2
        except AssertionError:
            self.message_user(request, 'Merci de sélectionner deux joueurs à fusionner', level=messages.WARNING)
            return HttpResponseRedirect(reverse('admin:statscollect_db_footballperson_changelist'))
        source, target = FootballPerson.objects.order_by_meeting_count(queryset[0], queryset[1])
        FootballPerson.objects.merge(source, target)
        self.message_user(request, "Joueur %s (%s) fusionné vers %s (%s)" % (source, source.uuid, target, target.uuid))
        self.message_user(request, "Joueur %s (%s) peut maintenant être supprimé" % (source, source.uuid))
        return HttpResponseRedirect(reverse('admin:statscollect_db_footballperson_changelist'))

    merge_players_action.short_description = "Fusionner les données de deux joueurs"

    def get_queryset(self, request):
        return FootballPerson.objects.filter(field__contains='FOOTBALL').order_by('-updated_at')


class FootballMeetingParticipantRelatedInline(admin.TabularInline):
    def get_formset(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request, obj=obj)
        return super(FootballMeetingParticipantRelatedInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        football_meeting = kwargs.pop('obj', None)
        formfield = super(FootballMeetingParticipantRelatedInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'person' and football_meeting:
            formfield.queryset = Person.objects.filter(
                teammeeting=football_meeting)
        return formfield


class FootballStatsInline(FootballMeetingParticipantRelatedInline):
    model = FootballPersonalStats


class RatingsInline(FootballMeetingParticipantRelatedInline):
    model = Rating


class TeamMeetingPersonInline(FootballMeetingParticipantRelatedInline):
    model = TeamMeetingPerson
    form = FootballTeamMeetingPersonInlineForm


class FootballMeetingAdmin(admin.ModelAdmin):
    # merged_inline_order = 'person_id'
    inlines = [TeamMeetingPersonInline, FootballStatsInline, RatingsInline]
    form = FootballMeetingForm


# Register your models here.
admin.site.register(RatingSource)
admin.site.register(FootballMeeting, FootballMeetingAdmin)
admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(FootballPerson, FootballPersonAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentInstance, InstanceAdmin)
admin.site.register(TournamentInstanceStep)
