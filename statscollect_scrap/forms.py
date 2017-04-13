from django import forms
from django.forms.widgets import Textarea
from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget

from statscollect_scrap import lookups
from statscollect_scrap import models


class ScrapAccessModeMixin(forms.Form):
    mode = forms.ChoiceField(
        choices=(('URL', 'Par adresse'), ('SELENIUM', 'Navigateur [WS only]'), ('MANUAL', 'Copier-coller')),
        initial='URL',
        required=True, label="Mode d'accès")


class ScrapIdentifierForm(ScrapAccessModeMixin, forms.ModelForm):
    identifier = forms.CharField(max_length=100, required=False,
                                 help_text='Identifiant du match ou de la journée dans l\'URL de la page à importer. Dans le doute, laissez ce champ vide et copiez l\'adresse complète dans scrapped_url')

    scraped_url = forms.URLField(max_length=300, required=False,
                                 help_text='Adresse HTTP complète de la page à importer')

    page_content = forms.CharField(required=False, widget=Textarea,
                                   help_text='Copier ici le code source de la page à traiter')

    scrap_again = forms.BooleanField(required=False,
                                     help_text='Cocher cette case pour forcer la réimportation')

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.instance.status == 'CREATED':
            if cleaned_data['mode'] == 'URL':
                if 'scrapper' in cleaned_data and cleaned_data['scrapper'].class_name != 'FakeScrapper':
                    if not ('scrapped_url' in cleaned_data or 'identifier' in cleaned_data):
                        raise forms.ValidationError('Either scrapped_url or identifier is required')
            elif cleaned_data['mode'] == 'MANUAL':
                if not cleaned_data['page_content']:
                    raise forms.ValidationError('Page content is required')


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
        fields = ('actual_tournament', 'actual_instance', 'actual_step', 'scrapper')


class ParticipantAdminForm(forms.ModelForm):
    actual_player = AutoCompleteSelectField(
        lookup_class=lookups.ParticipantLookup
    )

    class Meta(object):
        model = models.ScrappedGameSheetParticipant
        fields = '__all__'


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
        fields = '__all__'


class TeamMeetingDataForm(ScrapIdentifierForm):
    pass


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

    class Media:
        js = (
            '/static/statscollect_scrap/js/instance_lookup.js',
            '/static/statscollect_scrap/js/step_lookup.js',
            '/static/statscollect_scrap/js/gamesheetparticipant_dynac.js',
            '/static/statscollect_scrap/js/ratingsource_lookup.js',
        )


class ProcessedGameRatingSourceForm(forms.ModelForm):
    rating_source = AutoCompleteSelectField(
        lookup_class=lookups.RatingSourceLookup,
        allow_new=False,
        required=True,
        widget=AutoComboboxSelectWidget
    )

    class Media:
        js = (
            '/static/statscollect_scrap/js/ratingsource_lookup.js',
        )