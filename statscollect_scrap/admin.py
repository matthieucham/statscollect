from functools import partial

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from statscollect_scrap import models
from statscollect_scrap import forms
from statscollect_scrap import scrappers
from statscollect_scrap import translators
from statscollect_scrap import widgets
from statscollect_scrap import processors


class ScrappedEntityAdminMixin(object):
    processor = None

    def process_model(self, scrapped_entity, form):
        assert isinstance(scrapped_entity, models.ScrappedEntity)
        force_scrapping = form.cleaned_data.get('scrap_again', False)
        if scrapped_entity.status == 'CREATED' or force_scrapping:
            if scrapped_entity.scrapper.class_name == 'FakeScrapper':
                # Do nothing (no scrapping required)
                new_status = 'COMPLETE'
            else:
                # Scrap this new object !
                scrapped_result = self.processor.process(form, scrapped_entity.scrapper)
                if scrapped_result and len(scrapped_result) > 0:
                    # Delete previous scrap results if 'scrap_again'
                    if force_scrapping:
                        self.processor.cleanup_target_objects()
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
                    # scrapped_entity.scrapped_url = url_to_scrap
                    new_status = 'PENDING'
                else:
                    raise ValueError('The scrapping processor %s could not scrap any stat' % (
                        scrapped_entity.scrapper.class_name))
        elif scrapped_entity.status == 'PENDING':
            new_status = 'COMPLETE'
        else:
            new_status = 'AMENDED'

        scrapped_entity.status = new_status
        scrapped_entity.save()


class ScrappedModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'created_at', 'updated_at')
    actions = ['delete_complete']

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_scrap'] = True
        return super(ScrappedModelAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            ss = self.model.objects.get(pk=object_id)
            if ss.status == 'CREATED':
                extra_context['show_scrap'] = True
            else:
                extra_context['show_confirm'] = True
        else:
            extra_context['show_confirm'] = True
        return super(ScrappedModelAdmin, self).change_view(request, object_id, form_url, extra_context)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'scrapper':
            kwargs["queryset"] = models.FootballScrapper.objects.filter(category=self.scrapper_category)
        return super(ScrappedModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def delete_complete(self, request, queryset):
        self.model.objects.filter(status__in=['COMPLETE', 'AMENDED']).delete()
        self.message_user(request, "Entités %s avec status COMPLETE ou AMENDED effacées" %
                          self.model._meta.verbose_name_plural)

    delete_complete.short_description = "Effacer les entités COMPLETE ou AMENDED"


class ScrappedFootballGameResultInline(admin.StackedInline):
    model = models.ScrappedFootballGameResult
    extra = 0
    max_num = 0
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


class ScrappedFootballStepAdmin(ScrappedEntityAdminMixin, ScrappedModelAdmin):
    model = models.ScrappedFootballStep
    form = forms.ScrappedFootballStepForm
    inlines = [ScrappedFootballGameResultInline, ]
    scrapper_category = 'STEP'

    def save_model(self, request, obj, form, change):
        super(ScrappedFootballStepAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballStepProcessor(obj)
        self.process_model(obj, form)

    def save_related(self, request, form, formsets, change):
        super(ScrappedFootballStepAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedFootballStepTranslator().translate(form.instance, update_names=form.cleaned_data.get(
                'set_team_names', False))


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


class ScrappedGameSheetParticipantInline(admin.StackedInline):
    model = models.ScrappedGameSheetParticipant
    extra = 0
    form = forms.ParticipantAdminForm
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
    template = "admin/statscollect_scrap/scrappedgamesheet/edit_inline/stacked.html"

    class Media:
        css = {
            'all': (
                '/static/statscollect_scrap/css/scrap.css',
            )
        }


class ScrappedGameSheetAdmin(ScrappedEntityAdminMixin, ScrappedModelAdmin):
    form = forms.ScrappedGamesheetForm
    inlines = [ScrappedGameSheetParticipantInline, ]
    fields = (
        'actual_tournament', 'actual_instance', 'actual_step', 'actual_meeting', 'scrapper', 'mode', 'identifier',
        'scraped_url', 'page_content', 'scrap_again', 'set_current_teams')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            # self.form.declared_fields['actual_tournament'].required = False
            self.form.declared_fields['actual_instance'].required = False
            self.form.declared_fields['actual_step'].required = False
            self.form.declared_fields['actual_meeting'].required = False
            return self.readonly_fields + (
                'actual_tournament', 'actual_instance', 'actual_step', 'actual_meeting')
        return self.readonly_fields

    scrapper_category = 'SHEET'

    def save_model(self, request, obj, form, change):
        super(ScrappedGameSheetAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballGamesheetProcessor(obj)
        self.process_model(obj, form)

    def save_related(self, request, form, formsets, change):
        super(ScrappedGameSheetAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedGamesheetTranslator().translate(form.instance, form.cleaned_data.get(
                'set_current_teams', False))


class ScrappedPlayerStatsInline(admin.TabularInline):
    model = models.ScrappedPlayerStats
    extra = 0
    max_num = 0
    can_delete = False
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


class ScrappedTeamMeetingAdmin(ScrappedEntityAdminMixin, ScrappedModelAdmin):
    readonly_fields = ('teammeeting',)
    model = models.ScrappedTeamMeetingData
    form = forms.TeamMeetingDataForm
    fields = ('teammeeting', 'scrapper', 'mode', 'identifier', 'scraped_url', 'page_content', 'scrap_again')
    inlines = [ScrappedPlayerStatsInline, ]
    scrapper_category = 'STATS'

    def save_model(self, request, obj, form, change):
        super(ScrappedTeamMeetingAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballStatsProcessor(obj)
        self.process_model(obj, form)

    def save_related(self, request, form, formsets, change):
        super(ScrappedTeamMeetingAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedTeamMeetingDataTranslator().translate(form.instance)


class ExpectedRatingSourceAdmin(admin.ModelAdmin):
    list_display = ('tournament_instance', 'expected_sources')

    def expected_sources(self, obj):
        return ", ".join([p.__str__() for p in obj.rating_source.all()])


class ScrappedPlayerRatingsInline(admin.TabularInline):
    model = models.ScrappedPlayerRatings
    extra = 0
    readonly_fields = (
        'read_rating',
    )
    fields = (
        'teammeetingperson',
        'read_rating',
        'actual_rating',
    )

    def get_formset(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request, obj=obj)
        return super(ScrappedPlayerRatingsInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        scrapped_player_rating = kwargs.pop('obj', None)
        if db_field.name == 'teammeetingperson':
            kwargs['widget'] = widgets.ReadOnlySelectWidget()
        formfield = super(ScrappedPlayerRatingsInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'teammeetingperson' and scrapped_player_rating:
            formfield.queryset = models.TeamMeetingPerson.objects.filter(
                meeting=scrapped_player_rating.teammeeting)
        return formfield


class ScrappedRatingsAdmin(ScrappedEntityAdminMixin, ScrappedModelAdmin):
    readonly_fields = ('teammeeting', 'rating_source')
    model = models.ScrappedTeamMeetingRatings
    form = forms.TeamMeetingDataForm
    fields = ('teammeeting', 'rating_source', 'scrapper', 'mode', 'identifier', 'scraped_url',
              'page_content', 'scrap_again')
    inlines = [ScrappedPlayerRatingsInline, ]
    scrapper_category = 'RATING'

    def save_model(self, request, obj, form, change):
        super(ScrappedRatingsAdmin, self).save_model(request, obj, form, change)
        self.processor = scrappers.FootballRatingsProcessor(obj)
        self.process_model(obj, form)

    def save_related(self, request, form, formsets, change):
        super(ScrappedRatingsAdmin, self).save_related(request, form, formsets, change)
        if form.instance.status in ['COMPLETE', 'AMENDED']:
            translators.ScrappedRatingsTranslator().translate(form.instance)


# V2
class ProcessedGamePlayerInline(admin.TabularInline):
    model = models.ProcessedGameSheetPlayer
    extra = 0
    form = forms.GamesheetPlayerAdminForm
    fields = (
        'footballperson',
        'playtime',
        'goals_scored',
        'penalties_scored',
        'goals_assists',
        'penalties_assists',
        'goals_saves',
        'goals_conceded',
        'penalties_saved',
        'own_goals',
    )
    template = "admin/statscollect_scrap/processedgame/edit_inline/tabular.html"

    def has_add_permission(self, request):
        return False

    class Media:
        css = {
            'all': (
                '/static/statscollect_scrap/css/scrap.css',
            )
        }


class ProcessedRatingInline(admin.TabularInline):
    model = models.ProcessedGameRating
    extra = 0
    form = forms.GamesheetPlayerAdminForm
    readonly_fields = (
        'rating_source',
    )
    fields = (
        'footballperson',
        'rating_source',
        'rating',
    )
    template = "admin/statscollect_scrap/processedgame/edit_inline/tabular.html"

    def has_add_permission(self, request):
        return False

    class Media:
        css = {
            'all': (
                '/static/statscollect_scrap/css/scrap.css',
            )
        }


class AddProcessedRatingInline(ProcessedRatingInline):
    readonly_fields = []

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    class Media:
        css = {
            'all': (
                '/static/statscollect_scrap/css/scrap.css',
            )
        }


class ProcessedGameAdmin(admin.ModelAdmin):
    model = models.ProcessedGame
    list_display = ('__str__', 'status', 'created_at', 'updated_at')
    form = forms.ProcessedGameForm
    filter_horizontal = ('rating_ds', )
    inlines = [ProcessedGamePlayerInline, ProcessedRatingInline, AddProcessedRatingInline]
    fieldsets = (
        ('Step', {
            'fields': ('actual_tournament', 'actual_instance',
                       'actual_step',
                       )
        }),
        ('Data sheets', {
            'fields': ('gamesheet_ds', 'rating_ds',)
        }),
    )

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['status'] = 'CREATED'
        return super(ProcessedGameAdmin, self).add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['status'] = models.ProcessedGame.objects.get(pk=object_id).status
        return super(ProcessedGameAdmin, self).change_view(request, object_id, form_url=form_url,
                                                           extra_context=extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        if "_process" in request.POST:
            # handle the action on your obj
            processor = processors.GamesheetProcessor()
            processor.process(obj)

            redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts},
                                                 redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            return super(ProcessedGameAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        if "_process" in request.POST:
            # handle the action on your obj
            processor = processors.GamesheetProcessor()
            processor.process(obj)

            redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts},
                                                 redirect_url)
            return HttpResponseRedirect(redirect_url)
        elif "_store" in request.POST:
            translator = translators.ProcessedGameTranslator()
            translator.translate(obj)

            post_url = reverse('admin:%s_%s_changelist' %
                               (opts.app_label, opts.model_name),
                               current_app=self.admin_site.name)
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url)
            return HttpResponseRedirect(post_url)

        else:
            return super(ProcessedGameAdmin, self).response_change(request, obj)

    class Media:
        css = {
            'all': (
                '/static/statscollect_scrap/css/scrap.css',
            )
        }

# Register your models here.
# admin.site.register(models.FootballScrapper, FootballScrapperAdmin)
# admin.site.register(models.FootballRatingScrapper, FootballRatingScrapperAdmin)
admin.site.register(models.ExpectedRatingSource, ExpectedRatingSourceAdmin)
#admin.site.register(models.ScrappedFootballStep, ScrappedFootballStepAdmin)
#admin.site.register(models.ScrappedGameSheet, ScrappedGameSheetAdmin)
#admin.site.register(models.ScrappedTeamMeetingData, ScrappedTeamMeetingAdmin)
#admin.site.register(models.ScrappedTeamMeetingRatings, ScrappedRatingsAdmin)
# V2
admin.site.register(models.ProcessedGame, ProcessedGameAdmin)