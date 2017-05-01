# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statscollect_db', '__first__'),
        ('statscollect_scrap', '0002_datasheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('PENDING', 'PENDING'), ('COMPLETE', 'COMPLETE'), ('AMENDED', 'AMENDED')], default='CREATED', editable=False, max_length=8)),
                ('actual_instance', models.ForeignKey(help_text='Edition de cette compétition', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TournamentInstance')),
                ('actual_step', models.ForeignKey(help_text='Journée de cette édition', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TournamentInstanceStep')),
                ('actual_tournament', models.ForeignKey(help_text='Championnat ou compétition', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.Tournament')),
                ('gamesheet_ds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamesheet_processedgame', to='statscollect_scrap.ScrapedDataSheet')),
                ('rating_ds', models.ManyToManyField(related_name='ratingsheet_processedgame', to='statscollect_scrap.ScrapedDataSheet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessedGameRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scraped_name', models.CharField(editable=False, max_length=255)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, help_text='Note', max_digits=5, null=True)),
                ('footballperson', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.FootballPerson')),
                ('processed_game', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.ProcessedGame')),
                ('rating_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.RatingSource')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedGameSheetPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scraped_name', models.CharField(editable=False, max_length=255)),
                ('scraped_ratio', models.DecimalField(blank=True, decimal_places=1, help_text='Taux de correspondance entre nom lu et joueur préselectionné (%)', max_digits=4, null=True)),
                ('playtime', models.SmallIntegerField(default=0, help_text='Temps de jeu')),
                ('goals_scored', models.SmallIntegerField(default=0, help_text='Nombre de buts marqués (hors pénaltys)')),
                ('penalties_scored', models.SmallIntegerField(default=0, help_text='Nombre de pénaltys marqués')),
                ('goals_assists', models.SmallIntegerField(default=0, help_text='Nombre de passes décisives')),
                ('penalties_assists', models.SmallIntegerField(default=0, help_text='Nombre de pénaltys obtenus')),
                ('goals_saves', models.SmallIntegerField(default=0, help_text="Nombre d'arrêts")),
                ('goals_conceded', models.SmallIntegerField(default=0, help_text='Nombre de buts encaissés')),
                ('own_goals', models.SmallIntegerField(default=0, help_text='Nombre de buts contre son camp')),
                ('footballperson', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.FootballPerson')),
                ('processed_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.ProcessedGame')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedGameSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_date', models.DateTimeField(editable=False)),
                ('home_score', models.SmallIntegerField(editable=False)),
                ('away_score', models.SmallIntegerField(editable=False)),
                ('away_team', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='processed_away_games', to='statscollect_db.Team')),
                ('home_team', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='processed_home_games', to='statscollect_db.Team')),
                ('processed_game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.ProcessedGame')),
            ],
        ),
    ]