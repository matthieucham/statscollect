from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from statscollect_db.models import (
    RatingSource,
    Team,
    Tournament,
    TournamentInstance,
    TournamentInstanceStep,
    FootballPerson,
)


class ExpectedRatingSource(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    tournament_instance = models.ForeignKey(
        TournamentInstance, on_delete=models.CASCADE
    )
    rating_source = models.ManyToManyField(RatingSource, related_name="expected_set")


class ScrappedEntity(models.Model):
    STATUS_CHOICES = (
        ("CREATED", "CREATED"),
        ("PENDING", "PENDING"),
        ("COMPLETE", "COMPLETE"),
        ("AMENDED", "AMENDED"),
    )

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    # scrapped_url = models.URLField(max_length=300, blank=True, null=True,
    # help_text='Adresse HTTP complète de la page à importer')
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default="CREATED", editable=False
    )

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
    source = models.ForeignKey(
        RatingSource, editable=False, null=True, on_delete=models.CASCADE
    )
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
            self.source,
            self.content.get("home_team"),
            self.content.get("home_score", "?"),
            self.content.get("away_score", "?"),
            self.content.get("away_team"),
            self.content.get("match_date"),
        )

    class Meta:
        ordering = ["-match_date"]


class ProcessedGame(ScrappedEntity):
    actual_tournament = models.ForeignKey(
        Tournament, help_text="Championnat ou compétition", on_delete=models.CASCADE
    )
    actual_instance = models.ForeignKey(
        TournamentInstance,
        help_text="Edition de cette compétition",
        on_delete=models.CASCADE,
    )
    actual_step = models.ForeignKey(
        TournamentInstanceStep,
        help_text="Journée de cette édition",
        on_delete=models.CASCADE,
    )
    # Gamesheet
    gamesheet_ds = models.ForeignKey(
        ScrapedDataSheet,
        null=True,
        related_name="gamesheet_processedgame",
        on_delete=models.SET_NULL,
    )
    # rating sheets
    rating_ds = models.ManyToManyField(
        ScrapedDataSheet, related_name="ratingsheet_processedgame"
    )

    def __str__(self):
        return "[J%s] %s" % (self.actual_step, self.gamesheet_ds)


class ProcessedGameSummary(models.Model):
    # link to ProcessedGame
    processed_game = models.OneToOneField(ProcessedGame, on_delete=models.CASCADE)
    # Processed fields
    game_date = models.DateTimeField(editable=False)
    home_team = models.ForeignKey(
        Team,
        editable=False,
        related_name="processed_home_games",
        on_delete=models.CASCADE,
    )
    away_team = models.ForeignKey(
        Team,
        editable=False,
        related_name="processed_away_games",
        on_delete=models.CASCADE,
    )
    home_score = models.SmallIntegerField(editable=False)
    away_score = models.SmallIntegerField(editable=False)


class ProcessedGameSheetPlayer(models.Model):
    # link to ProcessedGame
    processed_game = models.ForeignKey(ProcessedGame, on_delete=models.CASCADE)
    # processed fields
    scraped_name = models.CharField(max_length=255, editable=False)
    scraped_ratio = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )
    footballperson = models.ForeignKey(
        FootballPerson, blank=True, null=True, on_delete=models.CASCADE
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    playtime = models.SmallIntegerField(default=0, help_text="Temps de jeu")
    goals_scored = models.SmallIntegerField(
        default=0, help_text="Nombre de buts marqués (hors pénaltys)"
    )
    penalties_scored = models.SmallIntegerField(
        default=0, help_text="Nombre de pénaltys marqués"
    )
    goals_assists = models.SmallIntegerField(
        default=0, help_text="Nombre de passes décisives"
    )
    penalties_assists = models.SmallIntegerField(
        default=0, help_text="Nombre de pénaltys obtenus"
    )
    goals_saves = models.SmallIntegerField(default=0, help_text="Nombre d'arrêts")
    goals_conceded = models.SmallIntegerField(
        default=0, help_text="Nombre de buts encaissés"
    )
    own_goals = models.SmallIntegerField(
        default=0, help_text="Nombre de buts contre son camp"
    )
    penalties_saved = models.SmallIntegerField(
        default=0, help_text="Nombre de pénaltys arrêtés"
    )

    def __str__(self):
        return "%s [%s]" % (self.scraped_name, self.scraped_ratio)


class ProcessedGameRating(models.Model):
    # link to ProcessedGame
    processed_game = models.ForeignKey(
        ProcessedGame, editable=False, on_delete=models.CASCADE
    )
    # link to RatingSource
    rating_source = models.ForeignKey(RatingSource, on_delete=models.CASCADE)
    # processed fields
    scraped_name = models.CharField(
        max_length=255, editable=False, blank=True, null=True
    )
    scraped_ratio = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )
    footballperson = models.ForeignKey(
        FootballPerson, blank=True, null=True, on_delete=models.CASCADE
    )
    rating = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text="Note"
    )

    def __str__(self):
        return "%s [%s]" % (self.scraped_name, self.scraped_ratio)


# V2 models
class ScrapedTeamWithPlayer(models.Model):
    team_name = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)
    content = JSONField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.team_name:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(ScrapedTeamWithPlayer, self).save(*args, **kwargs)

    def __str__(self):
        return self.team_name

    class Meta:
        ordering = ["team_name"]
