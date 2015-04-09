from django import forms

from selectable.forms import AutoCompleteSelectField

from statscollect_scrap import lookups
from statscollect_scrap import models


class ScrapIdentifierForm(forms.ModelForm):
    identifier = forms.CharField(max_length=8, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.instance.status == 'CREATED':
            if cleaned_data['scrapper'].class_name != 'FakeScrapper':
                if not cleaned_data['scrapped_url'] and not cleaned_data['identifier']:
                    raise forms.ValidationError('Either scrapped_url or identifier is required')


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
    set_team_names = forms.BooleanField(required=False)

    class Meta(object):
        model = models.ScrappedFootballStep
        fields = ('actual_tournament', 'actual_instance', 'actual_step', 'scrapper', 'identifier', 'scrapped_url',
                  'set_team_names')


class ParticipantAdminForm(forms.ModelForm):
    actual_player = AutoCompleteSelectField(
        lookup_class=lookups.ParticipantLookup
    )

    class Meta(object):
        model = models.ScrappedGameSheetParticipant


class ScrappedGamesheetForm(ScrapIdentifierForm):
    set_current_teams = forms.BooleanField(required=False)

    class Media:
        js = (
            '/static/statscollect_scrap/js/gamesheetparticipant_dynac.js',
        )

    class Meta:
        model = models.ScrappedGameSheet


class TeamMeetingDataForm(ScrapIdentifierForm):
    pass