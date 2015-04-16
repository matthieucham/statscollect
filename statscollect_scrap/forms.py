from django import forms
from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget

from statscollect_scrap import lookups
from statscollect_scrap import models


class ScrapIdentifierForm(forms.ModelForm):
    identifier = forms.CharField(max_length=8, required=False,
                                 help_text='Identifiant du match ou de la journée dans l\'URL de la page à importer. Dans le doute, laissez ce champ vide et copiez l\'adresse complète dans scrapped_url')

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.instance.status == 'CREATED':
            if 'scrapper' in cleaned_data and cleaned_data['scrapper'].class_name != 'FakeScrapper':
                if not ('scrapped_url' in cleaned_data or 'identifier' in cleaned_data):
                    raise forms.ValidationError('Either scrapped_url or identifier is required')


class ScrappedFootballStepForm(ScrapIdentifierForm):
    actual_instance = AutoCompleteSelectField(
        lookup_class=lookups.TournamentInstanceLookup,
        allow_new=False,
        required=True,
        widget=AutoComboboxSelectWidget
    )
    actual_step = AutoCompleteSelectField(
        lookup_class=lookups.TournamentStepLookup,
        allow_new=False,
        required=True,
        widget=AutoComboboxSelectWidget
    )
    set_team_names = forms.BooleanField(required=False,
                                        help_text='Cocher cette case pour mettre à jour les noms "longs" des équipes avec les données importées de cette page')

    class Media:
        js = (
            '/static/statscollect_scrap/js/instance_lookup.js',
            '/static/statscollect_scrap/js/step_lookup.js',
        )

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
    actual_meeting = AutoCompleteSelectField(
        lookup_class=lookups.MeetingLookup,
        allow_new=False,
        required=True,
        widget=AutoComboboxSelectWidget
    )

    set_current_teams = forms.BooleanField(required=False,
                                           help_text='Cocher cette case pour mettre à jour les équipes actuelles de ces joueurs avec les données importées')

    class Media:
        js = (
            '/static/statscollect_scrap/js/instance_lookup.js',
            '/static/statscollect_scrap/js/step_lookup.js',
            '/static/statscollect_scrap/js/meeting_lookup.js',
            '/static/statscollect_scrap/js/gamesheetparticipant_dynac.js',
        )

    class Meta:
        model = models.ScrappedGameSheet


class TeamMeetingDataForm(ScrapIdentifierForm):
    pass