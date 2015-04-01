from django.db import models
from django.db.models import F

from .meta_model import MetaModel
from statscollect_db.models import tournament_model

from .tournament_model import TournamentInstance, TournamentInstanceStep
from .team_model import Team
from .person_model import Person


class Meeting(MetaModel):
    tournament_instance = models.ForeignKey(TournamentInstance, related_name='meetings')
    # Some meetings are not linked to a step (cf single-step tournaments like a one-day race)
    tournament_step = models.ForeignKey(TournamentInstanceStep, related_name='meetings', null=True)
    date = models.DateTimeField()
    # concurrents : will be part of PersonalMeetingModel, when defined.
    # concurrents = models.ManyToManyField(Person, blank=True, null=True)

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
    participants = models.ManyToManyField(Person, through='TeamMeetingPerson', blank=True, null=True)

    def __str__(self):
        if self.home_result is None or self.away_result is None:
            return "%s vs %s [%s]" % (self.home_team.__str__(), self.away_team.__str__(), self.date)
        else:
            return "%s %i-%i %s [%s]" % (self.home_team.__str__(), self.home_result,
                                         self.away_result, self.away_team.__str__(),
                                         self.date)


class FootballMeeting(TeamMeeting):

    class Meta:
        proxy = True


class TeamMeetingPerson(models.Model):
    meeting = models.ForeignKey(TeamMeeting)
    person = models.ForeignKey(Person)
    played_for = models.ForeignKey(Team)

    # def save(self, force_insert=False, force_update=False, using=None,
    # update_fields=None):
    #     # First insert teammeetingperson
    #     super(TeamMeetingPerson, self).save(force_insert, force_update, using, update_fields)
    #     if self.person not in self.meeting.concurrents.all():
    #         self.meeting.concurrents.add(self.person)
    #         self.meeting.save()
    #
    # def delete(self, using=None):
    #     self.meeting.concurrents.remove(self.person)
    #     self.meeting.save()
    #     super(TeamMeetingPerson, self).delete()

    # TODO restriction du champ played_for aux Team home/away.

