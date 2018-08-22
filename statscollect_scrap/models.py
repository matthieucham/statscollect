from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from statscollect_db.models import RatingSource, Team, Tournament, TournamentInstance, \
    TournamentInstanceStep, FootballPerson


class ExpectedRatingSource(models.Model):
    tournament = models.ForeignKey(Tournament)
    tournament_instance = models.ForeignKey(
        TournamentInstance
    )
    rating_source = models.ManyToManyField(RatingSource, related_name='expected_set')


class ScrappedEntity(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'CREATED'),
        ('PENDING', 'PENDING'),
        ('COMPLETE', 'COMPLETE'),
        ('AMENDED', 'AMENDED'),
    )

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    # scrapped_url = models.URLField(max_length=300, blank=True, null=True,
    # help_text='Adresse HTTP complète de la page à importer')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='CREATED', editable=False)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(ScrappedEntity, self).save(args, kwargs)

    class Meta:
        abstract = True


# V2 models
class ScrapedDataSheet(models.Model):
    hash_url = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)
    source = models.ForeignKey(RatingSource, editable=False, null=True)
    content = JSONField()
    match_date = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.hash_url:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(ScrapedDataSheet, self).save(*args, **kwargs)

    def __str__(self):
        return "[%s] %s %s - %s %s (%s)" % (
            self.source, self.content['home_team'], self.content['home_score'] if 'home_score' in self.content else '?',
            self.content['away_score'] if 'away_score' in self.content else '?', self.content['away_team'],
            self.content['match_date'])

    class Meta:
        ordering = ['-match_date']


class ProcessedGame(ScrappedEntity):
    actual_tournament = models.ForeignKey(Tournament, help_text='Championnat ou compétition')
    actual_instance = models.ForeignKey(TournamentInstance, help_text='Edition de cette compétition')
    actual_step = models.ForeignKey(
        TournamentInstanceStep, help_text='Journée de cette édition')
    # Gamesheet
    gamesheet_ds = models.ForeignKey(ScrapedDataSheet, related_name='gamesheet_processedgame')
    # rating sheets
    rating_ds = models.ManyToManyField(ScrapedDataSheet, related_name='ratingsheet_processedgame')

    def __str__(self):
        return "[J%s] %s" % (self.actual_step, self.gamesheet_ds)


class ProcessedGameSummary(models.Model):
    # link to ProcessedGame
    processed_game = models.OneToOneField(ProcessedGame)
    # Processed fields
    game_date = models.DateTimeField(editable=False)
    home_team = models.ForeignKey(Team, editable=False, related_name='processed_home_games')
    away_team = models.ForeignKey(Team, editable=False, related_name='processed_away_games')
    home_score = models.SmallIntegerField(editable=False)
    away_score = models.SmallIntegerField(editable=False)


class ProcessedGameSheetPlayer(models.Model):
    # link to ProcessedGame
    processed_game = models.ForeignKey(ProcessedGame)
    # processed fields
    scraped_name = models.CharField(max_length=255, editable=False)
    scraped_ratio = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    footballperson = models.ForeignKey(FootballPerson, blank=True, null=True)
    team = models.ForeignKey(Team)
    playtime = models.SmallIntegerField(default=0, help_text='Temps de jeu')
    goals_scored = models.SmallIntegerField(default=0, help_text='Nombre de buts marqués (hors pénaltys)')
    penalties_scored = models.SmallIntegerField(default=0, help_text='Nombre de pénaltys marqués')
    goals_assists = models.SmallIntegerField(default=0, help_text='Nombre de passes décisives')
    penalties_assists = models.SmallIntegerField(default=0, help_text='Nombre de pénaltys obtenus')
    goals_saves = models.SmallIntegerField(default=0, help_text='Nombre d\'arrêts')
    goals_conceded = models.SmallIntegerField(default=0, help_text='Nombre de buts encaissés')
    own_goals = models.SmallIntegerField(default=0, help_text='Nombre de buts contre son camp')
    penalties_saved = models.SmallIntegerField(default=0, help_text='Nombre de pénaltys arrêtés')

    def __str__(self):
        return '%s [%s]' % (self.scraped_name, self.scraped_ratio)


class ProcessedGameRating(models.Model):
    # link to ProcessedGame
    processed_game = models.ForeignKey(ProcessedGame, editable=False)
    # link to RatingSource
    rating_source = models.ForeignKey(RatingSource)
    # processed fields
    scraped_name = models.CharField(max_length=255, editable=False, blank=True, null=True)
    scraped_ratio = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    footballperson = models.ForeignKey(FootballPerson, blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Note')

    def __str__(self):
        return '%s [%s]' % (self.scraped_name, self.scraped_ratio)