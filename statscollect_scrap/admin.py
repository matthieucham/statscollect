from django.contrib import admin
from django import forms

from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget

from statscollect_scrap import models
from statscollect_scrap import lookups
from statscollect_scrap import scrappers
from statscollect_scrap import translators


class ScrapIdentifierForm(forms.ModelForm):
    identifier = forms.CharField(max_length=8, required=True)

    def __init__(self, *args, **kwargs):
        super(ScrapIdentifierForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.scrapped_url:
            self.fields['identifier'].required = False


class ScrappedFootballGameResultInline(admin.StackedInline):
    model = models.ScrappedFootballGameResult
    extra = 0
    readonly_fields = (
        'read_game_date',
        'read_home_team',
        'ratio_home_team',
        'read_away_team',
        'ratio_away_team',
        'read_home_score',
        'read_away_score',
    )
    fieldsets = (
        (None, {
            'fields': (('read_game_date', 'actual_game_date'),)
        }),
        (None, {
            'fields': (
                ('read_home_team', 'actual_home_team', 'ratio_home_team'),
                ('read_home_score', 'actual_home_score')
            )
        }),
        (None, {
            'fields': (
                ('read_away_team', 'actual_away_team', 'ratio_away_team'),
                ('read_away_score', 'actual_away_score')
            )
        }),
    )


class ScrappedFootballStepForm(ScrapIdentifierForm):
    # actual_step = AutoCompleteSelectField(
    # lookup_class=lookups.TournamentStepLookup,
    # allow_new=True,
    # required=True,
    # widget=AutoComboboxSelectWidget
    # )
    #
    # class Media:
    # js = (
    # '/static/statscollect_scrap/js/step_lookup.js',
    # )

    # identifier = forms.CharField(max_length=8, required=True)

    # def __init__(self, *args, **kwargs):
    # super(ScrappedFootballStepForm, self).__init__(*args, **kwargs)
    # if self.instance and self.instance.scrapped_url:
    #         self.fields['identifier'].required = False

    class Meta(object):
        model = models.ScrappedFootballStep
        fields = ('actual_tournament', 'actual_instance', 'actual_step', 'scrapper', 'identifier', 'scrapped_url',)


class ScrappedFootballStepAdmin(admin.ModelAdmin):
    model = models.ScrappedFootballStep
    form = ScrappedFootballStepForm
    list_display = ('__str__', 'status')
    inlines = [ScrappedFootballGameResultInline, ]
    readonly_fields = ('scrapped_url',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'scrapper':
            kwargs["queryset"] = models.FootballScrapper.objects.filter(category='STEP')
        return super(ScrappedFootballStepAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.status = 'PENDING'
        else:
            if obj.status == 'PENDING':
                obj.status = 'COMPLETE'
            else:
                obj.status = 'AMENDED'

        super(ScrappedFootballStepAdmin, self).save_model(request, obj, form, change)
        if not change:
            # Scrap this new object !
            url_to_scrap = obj.scrapper.url_pattern % form.cleaned_data.get('identifier')
            scrapped_games = scrappers.FootballStepProcessor(obj.actual_step).process(url_to_scrap,
                                                                                      obj.scrapper.class_name)
            if scrapped_games and len(scrapped_games) > 0:
                for game in scrapped_games:
                    game_obj = models.ScrappedFootballGameResult()
                    game_obj.scrapped_step = obj
                    game_obj.actual_away_score = game.scrapped_game.away_team_goals
                    game_obj.actual_away_team = game.matching_away_team
                    game_obj.actual_game_date = game.scrapped_game.game_date
                    game_obj.actual_home_score = game.scrapped_game.home_team_goals
                    game_obj.actual_home_team = game.matching_home_team
                    game_obj.ratio_home_team = game.matching_home_ratio
                    game_obj.ratio_away_team = game.matching_away_ratio
                    game_obj.read_away_score = game.scrapped_game.away_team_goals
                    game_obj.read_away_team = game.scrapped_game.away_team_name
                    game_obj.read_game_date = game.scrapped_game.read_date
                    game_obj.read_home_score = game.scrapped_game.home_team_goals
                    game_obj.read_home_team = game.scrapped_game.home_team_name
                    game_obj.save()
                obj.scrapped_url = url_to_scrap
                obj.save()
            else:
                raise ValueError('The scrapping processor %s could not scrap any game result from the URL %s' % (
                    obj.scrapper.class_name, url_to_scrap))

    def save_related(self, request, form, formsets, change):
        super(ScrappedFootballStepAdmin, self).save_related(request, form, formsets, change)
        if change:
            translators.ScrappedFootballStepTranslator().translate(form.instance)


class FootballScrapperAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'class_name',
        'category',
    )


class ParticipantAdminForm(forms.ModelForm):
    actual_player = AutoCompleteSelectField(
        lookup_class=lookups.ParticipantLookup
    )

    class Meta(object):
        model = models.ScrappedGameSheetParticipant


class ScrappedGameSheetParticipantInline(admin.StackedInline):
    model = models.ScrappedGameSheetParticipant
    extra = 0
    form = ParticipantAdminForm
    readonly_fields = (
        'read_player',
        'read_team',
        'ratio_player',
    )
    fieldsets = (
        (None, {
            'fields': (
                ('read_player', 'actual_player', 'ratio_player'),
                ('read_team', 'actual_team')
            )
        }),
    )


class ScrappedGamesheetForm(ScrapIdentifierForm):
    set_current_teams = forms.BooleanField(required=False)
    # identifier = forms.CharField(max_length=8, required=True)

    # def __init__(self, *args, **kwargs):
    # super(ScrappedGamesheetForm, self).__init__(*args, **kwargs)
    # if self.instance and self.instance.scrapped_url:
    #         self.fields['identifier'].required = False

    class Media:
        js = (
            '/static/statscollect_scrap/js/gamesheetparticipant_dynac.js',
        )

    class Meta:
        model = models.ScrappedGameSheet


class ScrappedGameSheetAdmin(admin.ModelAdmin):
    form = ScrappedGamesheetForm
    list_display = ('__str__', 'status')
    inlines = [ScrappedGameSheetParticipantInline, ]

    fields = (
        'actual_tournament', 'actual_instance', 'actual_step', 'actual_meeting', 'scrapper', 'identifier',
        'scrapped_url',
        'set_current_teams')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + (
                'actual_tournament', 'actual_instance', 'actual_step', 'actual_meeting', 'scrapped_url')
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'scrapper':
            kwargs["queryset"] = models.FootballScrapper.objects.filter(category='SHEET')
        return super(ScrappedGameSheetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.status == 'PENDING':
            obj.status = 'COMPLETE'
        elif obj.status == 'COMPLETE':
            obj.status = 'AMENDED'
        super(ScrappedGameSheetAdmin, self).save_model(request, obj, form, change)
        if obj.status == 'CREATED':
            # Scrap this new object !
            url_to_scrap = obj.scrapper.url_pattern % form.cleaned_data.get('identifier')
            scrapped_participants = scrappers.FootballGamesheetProcessor(obj.actual_meeting).process(url_to_scrap,
                                                                                                     obj.scrapper.class_name)
            if scrapped_participants and len(scrapped_participants) > 0:
                for participant in scrapped_participants:
                    part_obj = models.ScrappedGameSheetParticipant()
                    part_obj.scrapped_game_sheet = obj
                    part_obj.actual_player = participant.matching_player
                    part_obj.actual_team = participant.matching_player_team
                    part_obj.ratio_player = participant.matching_ratio
                    part_obj.read_player = participant.participant.read_player
                    part_obj.read_team = participant.participant.read_team
                    part_obj.save()
                obj.status = 'PENDING'
                obj.scrapped_url = url_to_scrap
                super(ScrappedGameSheetAdmin, self).save_model(request, obj, form, change)
            else:
                raise ValueError('The scrapping processor %s could not scrap any game participant from the URL %s' % (
                    obj.scrapper.class_name, url_to_scrap))

    def save_related(self, request, form, formsets, change):
        super(ScrappedGameSheetAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedGamesheetTranslator().translate(form.instance, form.cleaned_data.get(
                'set_current_teams', False))


class TeamMeetingDataForm(ScrapIdentifierForm):
    pass


class ScrappedTeamMeetingAdmin(admin.ModelAdmin):
    readonly_fields = ('actual_teammeeting', 'scrapped_url')
    model = models.ScrappedTeamMeetingData
    form = TeamMeetingDataForm
    fields = ('actual_teammeeting', 'scrapper', 'identifier', 'scrapped_url')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'scrapper':
            kwargs["queryset"] = models.FootballScrapper.objects.filter(category='STATS')
        return super(ScrappedTeamMeetingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.
admin.site.register(models.FootballScrapper, FootballScrapperAdmin)
admin.site.register(models.ScrappedFootballStep, ScrappedFootballStepAdmin)
admin.site.register(models.ScrappedGameSheet, ScrappedGameSheetAdmin)
admin.site.register(models.ScrappedTeamMeetingData, ScrappedTeamMeetingAdmin)