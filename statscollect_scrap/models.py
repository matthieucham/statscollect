from django.db import models
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey
from statscollect_db.models import RatingSource, FootballTeam, Tournament, TournamentInstance, TournamentInstanceStep


class Scrapper(models.Model):
    name = models.CharField(max_length=20)
    class_name = models.CharField(max_length=30)

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
    scrapped_url = models.URLField(max_length=300)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='CREATED', editable=False)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(ScrappedEntity, self).save(args, kwargs)

    class Meta:
        abstract = True


class FootballScrappedEntity(ScrappedEntity):
    scrapper = models.ForeignKey(FootballScrapper)

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
    #actual_step = models.ForeignKey(TournamentInstanceStep, )
    actual_step = ChainedForeignKey(
        TournamentInstanceStep,
        chained_field='actual_instance',
        chained_model_field='tournament_instance',
        show_all=False,
        auto_choose=True
    )

    # def save(self, *args, **kwargs):
    #     """
    #     Check if step did not exist already
    #     """
    #     if self.actual_step is None:
    #         existing = TournamentInstanceStep.objects.filter(tournament_instance=self.actual_instance).filter(
    #             name__contains=self.name)
    #         assert (existing is None), 'A step with the name %s has already been registered for this tournament '
    #         'instance. Please enter a different name if you are scrapping a new step, '
    #         'or set this existing step as the actual step' % self.name
    #     super(ScrappedFootballStep, self).save(args, kwargs)

    def __str__(self):
        return "Step %s of %s" % (self.actual_step, self.actual_instance)


class ScrappedFootballGameResult(models.Model):
    scrapped_step = models.ForeignKey(ScrappedFootballStep)
    read_game_date = models.DateTimeField()
    read_home_team = models.CharField(max_length=50)
    read_away_team = models.CharField(max_length=50)
    read_home_score = models.SmallIntegerField()
    read_away_score = models.SmallIntegerField()
    actual_game_date = models.DateTimeField()
    actual_home_team = models.ForeignKey(FootballTeam, null=True, related_name='scrapped_home_games')
    actual_away_team = models.ForeignKey(FootballTeam, null=True, related_name='scrapped_away_games')
    actual_home_score = models.SmallIntegerField()
    actual_away_score = models.SmallIntegerField()
    ratio_home_team = models.DecimalField(max_digits=4, decimal_places=1)
    ratio_away_team = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return "[%s] %s %i - %i %s" % (self.read_game_date, self.read_home_team, self.read_home_score,
                                       self.read_away_score, self.read_away_team)