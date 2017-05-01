# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-26 19:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('statscollect_db', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpectedRatingSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_source', models.ManyToManyField(related_name='expected_set', to='statscollect_db.RatingSource')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.Tournament')),
                ('tournament_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TournamentInstance')),
            ],
        ),
        migrations.CreateModel(
            name='FootballScrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('class_name', models.CharField(max_length=30)),
                ('url_pattern', models.CharField(max_length=300)),
                ('category', models.CharField(choices=[('STEP', 'Journée'), ('SHEET', 'Feuille de match'), ('STATS', 'Statistiques'), ('RATING', 'Notes')], max_length=6)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScrappedFootballGameResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_game_date', models.CharField(max_length=50)),
                ('read_home_team', models.CharField(max_length=50)),
                ('read_away_team', models.CharField(max_length=50)),
                ('read_home_score', models.SmallIntegerField()),
                ('read_away_score', models.SmallIntegerField()),
                ('actual_game_date', models.DateTimeField(null=True)),
                ('actual_home_score', models.SmallIntegerField()),
                ('actual_away_score', models.SmallIntegerField()),
                ('ratio_home_team', models.DecimalField(decimal_places=1, max_digits=4)),
                ('ratio_away_team', models.DecimalField(decimal_places=1, max_digits=4)),
                ('actual_away_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrapped_away_games', to='statscollect_db.Team')),
                ('actual_home_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrapped_home_games', to='statscollect_db.Team')),
            ],
            options={
                'verbose_name': 'résultat',
            },
        ),
        migrations.CreateModel(
            name='ScrappedFootballStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('PENDING', 'PENDING'), ('COMPLETE', 'COMPLETE'), ('AMENDED', 'AMENDED')], default='CREATED', editable=False, max_length=8)),
                ('actual_instance', models.ForeignKey(help_text='Edition de cette compétition', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TournamentInstance')),
                ('actual_step', models.ForeignKey(help_text='Journée de cette édition', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TournamentInstanceStep')),
                ('actual_tournament', models.ForeignKey(help_text='Championnat ou compétition', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.Tournament')),
            ],
            options={
                'verbose_name_plural': 'imports de journées',
                'verbose_name': 'import de journée',
            },
        ),
        migrations.CreateModel(
            name='ScrappedGameSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('PENDING', 'PENDING'), ('COMPLETE', 'COMPLETE'), ('AMENDED', 'AMENDED')], default='CREATED', editable=False, max_length=8)),
                ('actual_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TournamentInstance')),
                ('actual_meeting', models.ForeignKey(help_text='Rencontre', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TeamMeeting')),
                ('actual_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TournamentInstanceStep')),
                ('actual_tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.Tournament')),
            ],
            options={
                'verbose_name_plural': 'imports de feuilles de match',
                'verbose_name': 'import de feuille de match',
            },
        ),
        migrations.CreateModel(
            name='ScrappedGameSheetParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_player', models.CharField(blank=True, help_text='Nom du joueur importé de la page lue', max_length=100)),
                ('read_team', models.CharField(blank=True, help_text="Nom de l'équipe ou du club, importé de la page lue", max_length=50)),
                ('ratio_player', models.DecimalField(blank=True, decimal_places=1, help_text='Taux de correspondance entre nom lu et joueur préselectionné (%)', max_digits=4, null=True)),
                ('actual_player', models.ForeignKey(help_text='Joueur réel', null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.Person')),
                ('actual_team', models.ForeignKey(help_text='Club ou équipe réelle', null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.Team')),
                ('scrapped_game_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.ScrappedGameSheet')),
            ],
            options={
                'verbose_name': 'joueur',
            },
        ),
        migrations.CreateModel(
            name='ScrappedPlayerRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_rating', models.CharField(help_text='Note lue', max_length=10)),
                ('actual_rating', models.DecimalField(blank=True, decimal_places=2, help_text='Note réelle', max_digits=5, null=True)),
            ],
            options={
                'verbose_name': 'note',
            },
        ),
        migrations.CreateModel(
            name='ScrappedPlayerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_playtime', models.CharField(default='0', help_text='Temps de jeu importé', max_length=4)),
                ('actual_playtime', models.SmallIntegerField(default=0, help_text='Temps de jeu réel')),
                ('read_goals_scored', models.CharField(default='0', help_text='Nombre importé de buts marqués (hors pénaltys)', max_length=4)),
                ('actual_goals_scored', models.SmallIntegerField(default=0, help_text='Nombre réel de buts marqués (hors pénaltys)')),
                ('read_penalties_scored', models.CharField(default='0', help_text='Nombre importé de pénaltys marqués', max_length=4)),
                ('actual_penalties_scored', models.SmallIntegerField(default=0, help_text='Nombre réel de pénaltys marqués')),
                ('read_assists', models.CharField(default='0', help_text='Nombre importé de passes décisives', max_length=4)),
                ('actual_assists', models.SmallIntegerField(default=0, help_text='Nombre réel de passes décisives')),
                ('read_penalties_assists', models.CharField(default='0', help_text='Nombre importé de pénaltys obtenus', max_length=4)),
                ('actual_penalties_assists', models.SmallIntegerField(default=0, help_text='Nombre réel de pénaltys obtenus')),
                ('read_saves', models.CharField(default='0', help_text="Nombre importé d'arrêts", max_length=4)),
                ('actual_saves', models.SmallIntegerField(default=0, help_text="Nombre réel d'arrêts")),
                ('read_conceded', models.CharField(default='0', help_text='Nombre importé de buts encaissés', max_length=4)),
                ('actual_conceded', models.SmallIntegerField(default=0, help_text='Nombre réel de buts encaissés')),
                ('read_own_goals', models.CharField(default='0', help_text='Nombre importé de buts contre son camp', max_length=4)),
                ('actual_own_goals', models.SmallIntegerField(default=0, help_text='Nombre réel de buts contre son camp')),
            ],
        ),
        migrations.CreateModel(
            name='ScrappedTeamMeetingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('PENDING', 'PENDING'), ('COMPLETE', 'COMPLETE'), ('AMENDED', 'AMENDED')], default='CREATED', editable=False, max_length=8)),
            ],
            options={
                'verbose_name_plural': 'imports de statistiques de match',
                'verbose_name': 'import de statistiques de match',
            },
        ),
        migrations.CreateModel(
            name='ScrappedTeamMeetingRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('PENDING', 'PENDING'), ('COMPLETE', 'COMPLETE'), ('AMENDED', 'AMENDED')], default='CREATED', editable=False, max_length=8)),
                ('rating_source', models.ForeignKey(help_text='Source de notation', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.RatingSource')),
            ],
            options={
                'verbose_name_plural': 'imports de notes',
                'verbose_name': 'import de notes',
            },
        ),
        migrations.CreateModel(
            name='FootballRatingScrapper',
            fields=[
                ('footballscrapper_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='statscollect_scrap.FootballScrapper')),
                ('rating_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.RatingSource')),
            ],
            options={
                'abstract': False,
            },
            bases=('statscollect_scrap.footballscrapper',),
        ),
        migrations.AddField(
            model_name='scrappedteammeetingratings',
            name='scrapper',
            field=models.ForeignKey(help_text="Choisir un robot d'importation correspondant à scrapped_url", null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.FootballScrapper'),
        ),
        migrations.AddField(
            model_name='scrappedteammeetingratings',
            name='teammeeting',
            field=models.ForeignKey(help_text='Rencontre', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TeamMeeting'),
        ),
        migrations.AddField(
            model_name='scrappedteammeetingdata',
            name='scrapper',
            field=models.ForeignKey(help_text="Choisir un robot d'importation correspondant à scrapped_url", null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.FootballScrapper'),
        ),
        migrations.AddField(
            model_name='scrappedteammeetingdata',
            name='teammeeting',
            field=models.ForeignKey(help_text='Rencontre', on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TeamMeeting'),
        ),
        migrations.AddField(
            model_name='scrappedplayerstats',
            name='teammeeting',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.ScrappedTeamMeetingData'),
        ),
        migrations.AddField(
            model_name='scrappedplayerstats',
            name='teammeetingperson',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TeamMeetingPerson'),
        ),
        migrations.AddField(
            model_name='scrappedplayerratings',
            name='scrapped_meeting',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.ScrappedTeamMeetingRatings'),
        ),
        migrations.AddField(
            model_name='scrappedplayerratings',
            name='teammeetingperson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.TeamMeetingPerson'),
        ),
        migrations.AddField(
            model_name='scrappedgamesheet',
            name='scrapper',
            field=models.ForeignKey(help_text="Choisir un robot d'importation correspondant à scrapped_url", null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.FootballScrapper'),
        ),
        migrations.AddField(
            model_name='scrappedfootballstep',
            name='scrapper',
            field=models.ForeignKey(help_text="Choisir un robot d'importation correspondant à scrapped_url", null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.FootballScrapper'),
        ),
        migrations.AddField(
            model_name='scrappedfootballgameresult',
            name='scrapped_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.ScrappedFootballStep'),
        ),
        migrations.AddField(
            model_name='footballscrapper',
            name='next_scrapper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_scrap.FootballScrapper'),
        ),
    ]
