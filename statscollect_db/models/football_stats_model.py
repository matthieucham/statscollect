from django.db import models

from .person_model import FootballPerson
from .meeting_model import TeamMeeting


class FootballPersonalStats(models.Model):
    player = models.ForeignKey(FootballPerson)
    meeting = models.ForeignKey(TeamMeeting)
    playtime = models.SmallIntegerField()
    goals_scored = models.SmallIntegerField()
    goals_assists = models.SmallIntegerField()
    penalties_scored = models.SmallIntegerField()
    penalties_awarded = models.SmallIntegerField()
    goals_saved = models.SmallIntegerField()
    goals_conceded = models.SmallIntegerField()