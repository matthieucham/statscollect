from django.db import models

from .person_model import Person
from .meeting_model import TeamMeeting


class FootballPersonalStats(models.Model):
    person = models.ForeignKey(Person)
    meeting = models.ForeignKey(TeamMeeting)
    playtime = models.SmallIntegerField(null=True)
    goals_scored = models.SmallIntegerField(null=True)
    goals_assists = models.SmallIntegerField(null=True)
    penalties_scored = models.SmallIntegerField(null=True)
    penalties_awarded = models.SmallIntegerField(null=True)
    goals_saved = models.SmallIntegerField(null=True)
    goals_conceded = models.SmallIntegerField(null=True)
    own_goals = models.SmallIntegerField(null=True)