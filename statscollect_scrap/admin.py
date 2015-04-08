from django.contrib import admin
from django import forms

from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget

from statscollect_scrap import models
from statscollect_scrap import lookups
from statscollect_scrap import scrappers
from statscollect_scrap import translators


class ScrapIdentifierForm(forms.ModelForm):
    identifier = forms.CharField(max_length=8, required=False)

    def __init__(self, *args, **kwargs):
        super(ScrapIdentifierForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.scrapped_url:
            self.fields['identifier'].required = False

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.instance.status == 'CREATED':
            if not cleaned_data['scrapped_url'] and not cleaned_data['identifier']:
                raise forms.ValidationError('Either scrapped_url or identifier is required')


class ScrappedEntityAdminMixin(object):
    scrapper_category = None
    processor = None

    def restrain_scrapper_category(self, db_field, **kwargs):
        if db_field.name == 'scrapper':
            kwargs["queryset"] = models.FootballScrapper.objects.filter(category=self.scrapper_category)
        return kwargs

    def process_model(self, scrapped_entity, form):
        assert isinstance(scrapped_entity, models.ScrappedEntity)
        if scrapped_entity.status == 'CREATED':
            # Scrap this new object !
            if form.cleaned_data.get('scrapped_url'):
                url_to_scrap = form.cleaned_data.get('scrapped_url')
            else:
                url_to_scrap = scrapped_entity.scrapper.url_pattern % form.cleaned_data.get('identifier')
            scrapped_result = self.processor.process(url_to_scrap, scrapped_entity.scrapper.class_name)
            if scrapped_result and len(scrapped_result) > 0:
                for scrapped in scrapped_result:
                    target = self.processor.create_target_object()
                    for key, value in scrapped.items():
                        if key.startswith('fk_'):
                            setattr(target, key[3:], value)
                        elif key.startswith('read_') or key.startswith('actual_') or key.startswith('ratio_'):
                            setattr(target, key, value)
                        else:
                            setattr(target, 'read_' + key, value)
                            setattr(target, 'actual_' + key, value)
                    target.save()
                scrapped_entity.scrapped_url = url_to_scrap
                new_status = 'PENDING'
            else:
                raise ValueError('The scrapping processor %s could not scrap any stat from the URL %s' % (
                    scrapped_entity.scrapper.class_name, url_to_scrap))
        elif scrapped_entity.status == 'PENDING':
            new_status = 'COMPLETE'
        else:
            new_status = 'AMENDED'

        scrapped_entity.status = new_status
        scrapped_entity.save()


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

    class Meta(object):
        model = models.ScrappedFootballStep
        fields = ('actual_tournament', 'actual_instance', 'actual_step', 'scrapper', 'identifier', 'scrapped_url',)


class ScrappedFootballStepAdmin(ScrappedEntityAdminMixin, admin.ModelAdmin):
    model = models.ScrappedFootballStep
    form = ScrappedFootballStepForm
    list_display = ('__str__', 'status')
    inlines = [ScrappedFootballGameResultInline, ]
    scrapper_category = 'STEP'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        restrained = self.restrain_scrapper_category(db_field, **kwargs)
        return super(ScrappedFootballStepAdmin, self).formfield_for_foreignkey(db_field, request, **restrained)

    def save_model(self, request, obj, form, change):
        super(ScrappedFootballStepAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballStepProcessor(obj)
        self.process_model(obj, form)

    def save_related(self, request, form, formsets, change):
        super(ScrappedFootballStepAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedFootballStepTranslator().translate(form.instance)


class FootballScrapperAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'class_name',
        'category',
    )


class FootballRatingScrapperAdmin(admin.ModelAdmin):
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

    class Media:
        js = (
            '/static/statscollect_scrap/js/gamesheetparticipant_dynac.js',
        )

    class Meta:
        model = models.ScrappedGameSheet


class ScrappedGameSheetAdmin(ScrappedEntityAdminMixin, admin.ModelAdmin):
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
                'actual_tournament', 'actual_instance', 'actual_step', 'actual_meeting')
        return self.readonly_fields

    scrapper_category = 'SHEET'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        restrained = self.restrain_scrapper_category(db_field, **kwargs)
        return super(ScrappedGameSheetAdmin, self).formfield_for_foreignkey(db_field, request, **restrained)

    def save_model(self, request, obj, form, change):
        super(ScrappedGameSheetAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballGamesheetProcessor(obj)
        self.process_model(obj, form)

    def save_related(self, request, form, formsets, change):
        super(ScrappedGameSheetAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedGamesheetTranslator().translate(form.instance, form.cleaned_data.get(
                'set_current_teams', False))


class TeamMeetingDataForm(ScrapIdentifierForm):
    pass


class ScrappedPlayerStatsInline(admin.TabularInline):
    model = models.ScrappedPlayerStats
    extra = 0
    readonly_fields = (
        'read_playtime',
        'read_goals_scored',
        'read_penalties_scored',
        'read_assists',
        'read_penalties_assists',
        'read_saves',
        'read_conceded',
        'read_own_goals',
    )
    fields = (
        'read_playtime',
        'actual_playtime',
        'read_goals_scored',
        'actual_goals_scored',
        'read_penalties_scored',
        'actual_penalties_scored',
        'read_assists',
        'actual_assists',
        'read_penalties_assists',
        'actual_penalties_assists',
        'read_saves',
        'actual_saves',
        'read_conceded',
        'actual_conceded',
        'read_own_goals',
        'actual_own_goals',
    )


class ScrappedTeamMeetingAdmin(ScrappedEntityAdminMixin, admin.ModelAdmin):
    readonly_fields = ('teammeeting',)
    model = models.ScrappedTeamMeetingData
    form = TeamMeetingDataForm
    fields = ('teammeeting', 'scrapper', 'identifier', 'scrapped_url')
    list_display = ('__str__', 'status')
    inlines = [ScrappedPlayerStatsInline, ]
    scrapper_category = 'STATS'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        restrained = self.restrain_scrapper_category(db_field, **kwargs)
        return super(ScrappedTeamMeetingAdmin, self).formfield_for_foreignkey(db_field, request, **restrained)

    def save_model(self, request, obj, form, change):
        super(ScrappedTeamMeetingAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballStatsProcessor(obj)
        self.process_model(obj, form)

    def save_related(self, request, form, formsets, change):
        super(ScrappedTeamMeetingAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedTeamMeetingDataTranslator().translate(form.instance)


class ExpectedRatingSourceAdmin(admin.ModelAdmin):
    list_display = ('tournament_instance', 'get_sources')

    def get_sources(self, obj):
        return ", ".join([p.__str__() for p in obj.rating_source.all()])


class ScrappedPlayerRatingsInline(admin.TabularInline):
    model = models.ScrappedPlayerRatings
    extra = 0
    readonly_fields = (
        'read_rating',
    )
    fields = (
        'read_rating',
        'actual_rating',
    )


class ScrappedRatingsAdmin(ScrappedEntityAdminMixin, admin.ModelAdmin):
    readonly_fields = ('teammeeting', 'rating_source')
    model = models.ScrappedTeamMeetingRatings
    form = TeamMeetingDataForm
    fields = ('teammeeting', 'rating_source', 'scrapper', 'identifier', 'scrapped_url')
    list_display = ('__str__', 'status')
    inlines = [ScrappedPlayerRatingsInline, ]
    scrapper_category = 'RATING'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        restrained = self.restrain_scrapper_category(db_field, **kwargs)
        return super(ScrappedRatingsAdmin, self).formfield_for_foreignkey(db_field, request, **restrained)

    def save_model(self, request, obj, form, change):
        super(ScrappedRatingsAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballRatingsProcessor(obj)
        self.process_model(obj, form)

    # def save_related(self, request, form, formsets, change):
    #     super(ScrappedRatingsAdmin, self).save_related(request, form, formsets, change)
    #     if form.instance.status in ['COMPLETE', 'AMENDED']:
    #         translators.ScrappedTeamMeetingDataTranslator().translate(form.instance)


# Register your models here.
admin.site.register(models.FootballScrapper, FootballScrapperAdmin)
admin.site.register(models.FootballRatingScrapper, FootballRatingScrapperAdmin)
admin.site.register(models.ExpectedRatingSource, ExpectedRatingSourceAdmin)
admin.site.register(models.ScrappedFootballStep, ScrappedFootballStepAdmin)
admin.site.register(models.ScrappedGameSheet, ScrappedGameSheetAdmin)
admin.site.register(models.ScrappedTeamMeetingData, ScrappedTeamMeetingAdmin)
admin.site.register(models.ScrappedTeamMeetingRatings, ScrappedRatingsAdmin)