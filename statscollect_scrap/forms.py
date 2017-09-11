from django import forms
from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget, AutoCompleteSelectMultipleField, AutoComboboxSelectMultipleWidget

from statscollect_scrap import lookups
from statscollect_scrap import models


class ProcessedGameForm(forms.ModelForm):
    actual_instance = AutoCompleteSelectField(
        lookup_class=lookups.TournamentInstanceLookup,
        allow_new=False,
        required=True,
        widget=AutoComboboxSelectWidget,

    )
    actual_step = AutoCompleteSelectField(
        lookup_class=lookups.TournamentStepLookup,
        allow_new=False,
        required=True,
        widget=AutoComboboxSelectWidget
    )
    gamesheet_ds = AutoCompleteSelectField(
        lookup_class=lookups.GamesheetLookup,
        allow_new=False,
        required=True,
        widget=AutoComboboxSelectWidget
    )
    rating_ds = AutoCompleteSelectMultipleField(
        lookup_class=lookups.RatingsheetLookup,
        required=False,
        widget=AutoComboboxSelectMultipleWidget
    )

    class Media:
        js = (
            '/static/statscollect_scrap/js/instance_lookup.js',
            '/static/statscollect_scrap/js/step_lookup.js',
            '/static/statscollect_scrap/js/ratingsheet_lookup.js',
        )


class GamesheetPlayerAdminForm(forms.ModelForm):
    footballperson = AutoCompleteSelectField(
        lookup_class=lookups.ParticipantLookup,
        required=True
    )

    class Meta(object):
        model = models.ProcessedGameSheetPlayer
        fields = '__all__'