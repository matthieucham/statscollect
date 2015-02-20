from django.db import models
from django.db.models import F

from .meta_model import MetaModel
from statscollect_db.models import tournament_model

from .tournament_model import TournamentInstance, TournamentInstanceStep
from .team_model import Team
from .person_model import Person


class Meeting(MetaModel):
    tournament_instance = models.ForeignKey(TournamentInstance)
    # Some meetings are not linked to a step (cf single-step tournaments like a one-day race)
    tournament_step = models.ForeignKey(TournamentInstanceStep, null=True)
    date = models.DateTimeField()

    def __str__(self):
        if self.teammeetingmodel:
            return self.teammeetingmodel.__str__()
        else:
            return self.tournament_instance.__str__()


class TeamMeeting(Meeting):
    home_team = models.ForeignKey(Team, related_name='meetings_home')
    home_result = models.PositiveSmallIntegerField(blank=True, null=True)
    away_team = models.ForeignKey(Team, related_name='meetings_away')
    away_result = models.PositiveSmallIntegerField(blank=True, null=True)
    participants = models.ManyToManyField(Person, through='TeamMeetingPerson', blank=True, null=True, symmetrical=False)

    def __str__(self):
        return self.home_team.__str__() + ' vs ' + self.away_team.__str__()


class FootballMeeting(TeamMeeting):

    class Meta:
        proxy = True


class TeamMeetingPerson(models.Model):
    meeting = models.ForeignKey(TeamMeeting)
    person = models.ForeignKey(Person)
    played_for = models.ForeignKey(Team)

    # TODO restriction du champ played_for aux Team home/away.

