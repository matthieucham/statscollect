from django.db import models

from .person_model import Person
from .meeting_model import TeamMeeting


class FootballPersonalStats(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    meeting = models.ForeignKey(TeamMeeting, on_delete=models.CASCADE)
    playtime = models.SmallIntegerField(blank=True, null=True)
    goals_scored = models.SmallIntegerField(blank=True, null=True)
    goals_assists = models.SmallIntegerField(blank=True, null=True)
    penalties_scored = models.SmallIntegerField(blank=True, null=True)
    penalties_awarded = models.SmallIntegerField(blank=True, null=True)
    goals_saved = models.SmallIntegerField(blank=True, null=True)
    goals_conceded = models.SmallIntegerField(blank=True, null=True)
    own_goals = models.SmallIntegerField(blank=True, null=True)
    penalties_saved = models.SmallIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(FootballPersonalStats, self).save(*args, **kwargs)
        self.meeting.save()

    class Meta:
        verbose_name = "statistiques (football)"
        verbose_name_plural = "statistiques (football)"
