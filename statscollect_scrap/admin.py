from functools import partial

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.urls import reverse
from django.http import HttpResponseRedirect

from statscollect_scrap import models
from statscollect_scrap import forms
from statscollect_scrap import translators
from statscollect_scrap import processors


# V2
class ProcessedGamePlayerInline(admin.TabularInline):
    model = models.ProcessedGameSheetPlayer
    extra = 0
    fields = (
        "footballperson",
        "playtime",
        "goals_scored",
        "penalties_scored",
        "goals_assists",
        "penalties_assists",
        "goals_saves",
        "goals_conceded",
        "penalties_saved",
        "own_goals",
    )
    autocomplete_fields = ["footballperson"]
    template = "admin/statscollect_scrap/processedgame/edit_inline/tabular.html"

    def has_add_permission(self, request):
        return False

    # class Media:
    #     css = {"all": ("/static/statscollect_scrap/css/scrap.css",)}


class ProcessedRatingInline(admin.TabularInline):
    model = models.ProcessedGameRating
    extra = 0
    # readonly_fields = ("rating_source",)
    fields = (
        "footballperson",
        "rating_source",
        "rating",
    )
    template = "admin/statscollect_scrap/processedgame/edit_inline/tabular.html"
    autocomplete_fields = ["footballperson", "rating_source"]

    def has_add_permission(self, request):
        return True

    # class Media:
    #     css = {"all": ("/static/statscollect_scrap/css/scrap.css",)}


# class AddProcessedRatingInline(ProcessedRatingInline):
#     readonly_fields = []

#     def has_add_permission(self, request):
#         return True

#     def has_change_permission(self, request, obj=None):
#         return False

#     # class Media:
#     #     css = {"all": ("/static/statscollect_scrap/css/scrap.css",)}


class ProcessedGameAdmin(admin.ModelAdmin):
    model = models.ProcessedGame
    list_display = ("__str__", "status", "created_at", "updated_at")
    form = forms.ProcessedGameForm
    filter_horizontal = ("rating_ds",)
    inlines = [
        ProcessedGamePlayerInline,
        ProcessedRatingInline,
        # AddProcessedRatingInline,
    ]
    fieldsets = (
        (
            "Step",
            {
                "fields": (
                    "actual_tournament",
                    "actual_instance",
                    "actual_step",
                )
            },
        ),
        (
            "Data sheets",
            {
                "fields": (
                    "gamesheet_ds",
                    "rating_ds",
                )
            },
        ),
    )
    autocomplete_fields = [
        "rating_ds",
    ]

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["status"] = "CREATED"
        return super(ProcessedGameAdmin, self).add_view(
            request, extra_context=extra_context
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["status"] = models.ProcessedGame.objects.get(pk=object_id).status
        return super(ProcessedGameAdmin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context
        )

    def response_add(self, request, obj, post_url_continue=None):
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        if "_process" in request.POST:
            # handle the action on your obj
            processor = processors.GamesheetProcessor()
            processor.process(obj)

            redirect_url = reverse(
                "admin:%s_%s_change" % (opts.app_label, opts.model_name),
                args=(pk_value,),
                current_app=self.admin_site.name,
            )
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
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

            redirect_url = reverse(
                "admin:%s_%s_change" % (opts.app_label, opts.model_name),
                args=(pk_value,),
                current_app=self.admin_site.name,
            )
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)
        elif "_store" in request.POST:
            translator = translators.ProcessedGameTranslator()
            translator.translate(obj)

            post_url = reverse(
                "admin:%s_%s_changelist" % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, post_url
            )
            return HttpResponseRedirect(post_url)

        else:
            return super(ProcessedGameAdmin, self).response_change(request, obj)

    class Media:
        css = {"all": ("/static/statscollect_scrap/css/scrap.css",)}


class ScrapedDataSheetAdmin(admin.ModelAdmin):
    model = models.ScrapedDataSheet
    search_fields = ["content__home_team", "content__away_team"]
    ordering = ["-match_date"]


# V2
admin.site.register(models.ProcessedGame, ProcessedGameAdmin)
admin.site.register(models.ScrapedDataSheet, ScrapedDataSheetAdmin)
