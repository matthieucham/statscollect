from django.contrib import admin
from django import forms

from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget

from statscollect_scrap import models
from statscollect_scrap import lookups
from statscollect_scrap import scrappers
from statscollect_scrap import translators


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


class ScrappedFootballStepForm(forms.ModelForm):
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

    class Meta(object):
        model = models.ScrappedFootballStep
        fields = ('actual_tournament', 'actual_instance', 'actual_step', 'scrapper', 'scrapped_url',)


class ScrappedFootballStepAdmin(admin.ModelAdmin):
    model = models.ScrappedFootballStep
    form = ScrappedFootballStepForm
    list_display = ('__str__', 'status')
    inlines = [ScrappedFootballGameResultInline, ]

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

            scrapped_games = scrappers.FootballStepProcessor(obj.actual_step).process(obj.scrapped_url,
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
            else:
                raise ValueError('The scrapping processor %s could not scrap any game result from the URL %s' % (
                    obj.scrapper.class_name, obj.scrapped_url))

    def save_related(self, request, form, formsets, change):
        super(ScrappedFootballStepAdmin, self).save_related(request, form, formsets, change)
        if change:
            translators.ScrappedFootballStepTranslator().translate(form.instance)
            # translators.ScrappedFootballStepTranslator().prepare_related(form.instance)


class FootballScrapperAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'class_name',
        'category',
    )


class ScrappedGameSheetParticipantInline(admin.StackedInline):
    model = models.ScrappedGameSheetParticipant
    extra = 0
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


class ScrappedGameSheetAdmin(admin.ModelAdmin):
    model = models.ScrappedGameSheet
    list_display = ('__str__', 'status')
    inlines = [ScrappedGameSheetParticipantInline, ]

    fields = ('actual_tournament', 'actual_instance', 'actual_step', 'actual_meeting', 'scrapper', 'scrapped_url',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('actual_tournament', 'actual_instance', 'actual_step', 'actual_meeting')
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'scrapper':
            kwargs["queryset"] = models.FootballScrapper.objects.filter(category='SHEET')
        return super(ScrappedGameSheetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.
admin.site.register(models.FootballScrapper, FootballScrapperAdmin)
admin.site.register(models.ScrappedFootballStep, ScrappedFootballStepAdmin)
admin.site.register(models.ScrappedGameSheet, ScrappedGameSheetAdmin)