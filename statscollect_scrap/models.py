from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from smart_selects.db_fields import ChainedForeignKey
from statscollect_db.models import RatingSource, Team, Tournament, TournamentInstance, \
    TournamentInstanceStep, TeamMeeting, Person, TeamMeetingPerson


class Scrapper(models.Model):
    name = models.CharField(max_length=20)
    class_name = models.CharField(max_length=30)
    next_scrapper = models.ForeignKey('self', blank=True, null=True)
    url_pattern = models.CharField(max_length=300)

    def __str__(self):
        return self.class_name

    class Meta:
        abstract = True


class FootballScrapper(Scrapper):
    CATEGORY_CHOICE = (
        ('STEP', 'Journée'),
        ('SHEET', 'Feuille de match'),
        ('STATS', 'Statistiques'),
        ('RATING', 'Notes'),
    )

    category = models.CharField(max_length=6, choices=CATEGORY_CHOICE)


class FootballRatingScrapper(FootballScrapper):
    source = models.ForeignKey(RatingSource)

    def save(self, *args, **kwargs):
        self.category = 'RATING'
        super(FootballRatingScrapper, self).save(*args, **kwargs)


class ScrappedEntity(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'CREATED'),
        ('PENDING', 'PENDING'),
        ('COMPLETE', 'COMPLETE'),
        ('AMENDED', 'AMENDED'),
    )

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    scrapped_url = models.URLField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='CREATED', editable=False)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(ScrappedEntity, self).save(args, kwargs)

    class Meta:
        abstract = True


class FootballScrappedEntity(ScrappedEntity):
    scrapper = models.ForeignKey(FootballScrapper, null=True)

    def clean(self):
        if self.status != 'CREATED':
            if not self.scrapped_url:
                raise ValidationError('Scrapped URL is required')
            if not self.scrapper:
                raise ValidationError('A scrapper is required')

    class Meta:
        abstract = True


class ScrappedFootballStep(FootballScrappedEntity):
    actual_tournament = models.ForeignKey(Tournament)
    actual_instance = ChainedForeignKey(
        TournamentInstance,
        chained_field='actual_tournament',
        chained_model_field='tournament',
        show_all=False,
        auto_choose=True
    )
    actual_step = ChainedForeignKey(
        TournamentInstanceStep,
        chained_field='actual_instance',
        chained_model_field='tournament_instance',
        show_all=False,
        auto_choose=True
    )

    def __str__(self):
        return "Step %s of %s" % (self.actual_step, self.actual_instance)


class ScrappedFootballGameResult(models.Model):
    scrapped_step = models.ForeignKey(ScrappedFootballStep)
    read_game_date = models.CharField(max_length=50)
    read_home_team = models.CharField(max_length=50)
    read_away_team = models.CharField(max_length=50)
    read_home_score = models.SmallIntegerField()
    read_away_score = models.SmallIntegerField()
    actual_game_date = models.DateTimeField(null=True)
    actual_home_team = models.ForeignKey(Team, null=True, related_name='scrapped_home_games')
    actual_away_team = models.ForeignKey(Team, null=True, related_name='scrapped_away_games')
    actual_home_score = models.SmallIntegerField()
    actual_away_score = models.SmallIntegerField()
    ratio_home_team = models.DecimalField(max_digits=4, decimal_places=1)
    ratio_away_team = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return "[%s] %s %i - %i %s" % (self.read_game_date, self.read_home_team, self.read_home_score,
                                       self.read_away_score, self.read_away_team)


class ScrappedGameSheet(FootballScrappedEntity):
    actual_tournament = models.ForeignKey(Tournament)
    actual_instance = ChainedForeignKey(
        TournamentInstance,
        chained_field='actual_tournament',
        chained_model_field='tournament',
        show_all=False,
        auto_choose=True
    )
    actual_step = ChainedForeignKey(
        TournamentInstanceStep,
        chained_field='actual_instance',
        chained_model_field='tournament_instance',
        show_all=False,
        auto_choose=True
    )
    actual_meeting = ChainedForeignKey(
        TeamMeeting,
        chained_field='actual_step',
        chained_model_field='tournament_step',
        show_all=False,
        auto_choose=True
    )

    def __str__(self):
        return self.actual_meeting.__str__()


class ScrappedGameSheetParticipant(models.Model):
    scrapped_game_sheet = models.ForeignKey(ScrappedGameSheet)
    read_player = models.CharField(max_length=100, blank=True)
    actual_player = models.ForeignKey(Person, null=True)
    read_team = models.CharField(max_length=50, blank=True)
    actual_team = models.ForeignKey(Team, null=True)
    ratio_player = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return self.read_player


class ScrappedTeamMeetingData(FootballScrappedEntity):
    actual_teammeeting = models.ForeignKey(TeamMeeting)


class ScrappedPlayerStats(models.Model):
    teammeeting = models.ForeignKey(ScrappedTeamMeetingData)
    actual_teammeetingperson = models.ForeignKey(TeamMeetingPerson, null=True)
    read_player = models.CharField(max_length=100)
    ratio_player = models.DecimalField(max_digits=4, decimal_places=1)
    read_playtime = models.CharField(max_length=4)
    actual_playtime = models.SmallIntegerField()
    read_goals_scored = models.CharField(max_length=4)
    actual_goals_scored = models.SmallIntegerField()
    read_penalties_scored = models.CharField(max_length=4)
    actual_penalties_scored = models.SmallIntegerField()
    read_assists = models.CharField(max_length=4)
    actual_assists = models.SmallIntegerField()
    read_penalties_assists = models.CharField(max_length=4)
    actual_penalties_assists = models.SmallIntegerField()
    read_saves = models.CharField(max_length=4)
    actual_saves = models.SmallIntegerField()
    read_conceded = models.CharField(max_length=4)
    actual_conceded = models.SmallIntegerField()
    read_own_goals = models.CharField(max_length=4)
    actual_own_goals = models.SmallIntegerField()

    def __str__(self):
        return self.read_player