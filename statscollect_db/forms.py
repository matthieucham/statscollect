from django import forms
from django.contrib import admin
from django.db.models.fields.related import ManyToManyRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, FilteredSelectMultiple

from statscollect_db.models import Team, FootballTeam, FootballPerson, FootballMeeting, FootballPersonalStats, \
    TeamMeetingPerson


class FootballPersonForm(forms.ModelForm):
    current_teams = forms.ModelMultipleChoiceField(
        FootballTeam.objects.all(),
        widget=FilteredSelectMultiple('current teams', False),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FootballPersonForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            teams_values_list = self.instance.current_teams.values_list('pk', flat=True)
            self.initial['current_teams'] = teams_values_list

    def save(self, *args, **kwargs):
        instance = super(FootballPersonForm, self).save(*args, **kwargs)
        if instance.pk:
            #update
            for team in instance.current_teams.all():
                if team not in self.cleaned_data['current_teams']:
                    instance.current_teams.remove(team)
            for team in self.cleaned_data['current_teams']:
                if team not in instance.current_teams.all():
                    instance.current_teams.add(team)
        else:
            #create
            instance.save()
            for team in self.cleaned_data['current_teams']:
                instance.current_teams.add(team)
        return instance


class FootballTeamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FootballTeamForm, self).__init__(*args, **kwargs)
        self.fields['current_members'].queryset = FootballPerson.objects.all()


class FootballMeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FootballMeetingForm, self).__init__(*args, **kwargs)
        self.fields['home_team'].queryset = FootballTeam.objects.all()
        self.fields['away_team'].queryset = FootballTeam.objects.all()


class FootballTeamMeetingPersonInlineForm(forms.ModelForm):
    class Meta:
        model = TeamMeetingPerson
        fields = ('person', 'played_for')

    def __init__(self, *args, **kwargs):
        super(FootballTeamMeetingPersonInlineForm, self).__init__(*args, **kwargs)
        self.fields['played_for'].queryset = FootballTeam.objects.all()


