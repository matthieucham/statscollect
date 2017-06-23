# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import django.utils.timezone
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FootballPersonalStats',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('playtime', models.SmallIntegerField(blank=True, null=True)),
                ('goals_scored', models.SmallIntegerField(blank=True, null=True)),
                ('goals_assists', models.SmallIntegerField(blank=True, null=True)),
                ('penalties_scored', models.SmallIntegerField(blank=True, null=True)),
                ('penalties_awarded', models.SmallIntegerField(blank=True, null=True)),
                ('goals_saved', models.SmallIntegerField(blank=True, null=True)),
                ('goals_conceded', models.SmallIntegerField(blank=True, null=True)),
                ('own_goals', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'statistiques (football)',
                'verbose_name': 'statistiques (football)',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('usual_name', models.CharField(blank=True, max_length=50)),
                ('birth', models.DateField(blank=True, null=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, default='M')),
                ('rep_country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('field', models.CharField(choices=[('FOOTBALL', 'Football')], max_length=10)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], max_length=10, default='ACTIVE')),
                ('migration_id', models.CharField(unique=True, null=True, max_length=35)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('original_rating', models.DecimalField(null=True, decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'note',
            },
        ),
        migrations.CreateModel(
            name='RatingSource',
            fields=[
                ('uuid', models.UUIDField(unique=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('code', models.CharField(serialize=False, max_length=8, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('website', models.CharField(blank=True, max_length=400)),
                ('field', models.CharField(blank=True, choices=[('FOOTBALL', 'Football')], max_length=10)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('type', models.CharField(choices=[('10CLASSIC', 'Classical 0-10'), ('6GERMAN', 'German 1-6')], max_length=10, default='10CLASSIC')),
            ],
            options={
                'verbose_name_plural': 'sources de notes',
                'verbose_name': 'source de notes',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=50)),
                ('field', models.CharField(choices=[('FOOTBALL', 'Football'), ('CYCLING', 'Cycling')], max_length=10)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('migration_id', models.CharField(unique=True, null=True, max_length=35)),
            ],
            options={
                'ordering': ['-country', 'name'],
            },
        ),
        migrations.CreateModel(
            name='TeamMeetingPerson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('field', models.CharField(choices=[('FOOTBALL', 'Football')], max_length=10)),
                ('type', models.CharField(choices=[('NAT', 'National'), ('INT', 'International')], max_length=3)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
            ],
            options={
                'verbose_name': 'compétition',
            },
        ),
        migrations.CreateModel(
            name='TournamentInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('ONGOING', 'Ongoing'), ('ARCHIVED', 'Archived')], max_length=8, default='ARCHIVED')),
                ('tournament', models.ForeignKey(to='statscollect_db.Tournament')),
            ],
            options={
                'verbose_name_plural': 'éditions de compétition',
                'verbose_name': 'édition de compétition',
            },
        ),
        migrations.CreateModel(
            name='TournamentInstanceStep',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('tournament_instance', models.ForeignKey(to='statscollect_db.TournamentInstance', related_name='steps')),
            ],
            options={
                'verbose_name_plural': 'journées de compétition',
                'verbose_name': 'journée de compétition',
            },
        ),
        migrations.CreateModel(
            name='FootballPerson',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, to='statscollect_db.Person', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(null=True, choices=[('G', 'Gardien'), ('D', 'Défenseur'), ('M', 'Milieu'), ('A', 'Attaquant')], max_length=1)),
            ],
            options={
                'ordering': ['last_name', 'usual_name', 'first_name'],
                'verbose_name': 'footballeur',
            },
            bases=('statscollect_db.person',),
        ),
        migrations.CreateModel(
            name='TeamMeeting',
            fields=[
                ('meeting_ptr', models.OneToOneField(parent_link=True, to='statscollect_db.Meeting', serialize=False, auto_created=True, primary_key=True)),
                ('home_result', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('away_result', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('statscollect_db.meeting',),
        ),
        migrations.AddField(
            model_name='teammeetingperson',
            name='person',
            field=models.ForeignKey(to='statscollect_db.Person'),
        ),
        migrations.AddField(
            model_name='teammeetingperson',
            name='played_for',
            field=models.ForeignKey(to='statscollect_db.Team'),
        ),
        migrations.AddField(
            model_name='team',
            name='current_members',
            field=models.ManyToManyField(related_name='current_teams', blank=True, to='statscollect_db.Person'),
        ),
        migrations.AddField(
            model_name='rating',
            name='meeting',
            field=models.ForeignKey(to='statscollect_db.Meeting'),
        ),
        migrations.AddField(
            model_name='rating',
            name='person',
            field=models.ForeignKey(to='statscollect_db.Person'),
        ),
        migrations.AddField(
            model_name='rating',
            name='source',
            field=models.ForeignKey(to='statscollect_db.RatingSource'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='tournament_instance',
            field=models.ForeignKey(to='statscollect_db.TournamentInstance', related_name='meetings'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='tournament_step',
            field=models.ForeignKey(related_name='meetings', null=True, to='statscollect_db.TournamentInstanceStep'),
        ),
        migrations.AddField(
            model_name='footballpersonalstats',
            name='person',
            field=models.ForeignKey(to='statscollect_db.Person'),
        ),
        migrations.CreateModel(
            name='FootballTeam',
            fields=[
            ],
            options={
                'verbose_name_plural': 'clubs (football)',
                'proxy': True,
                'verbose_name': 'club (football)',
            },
            bases=('statscollect_db.team',),
        ),
        migrations.AddField(
            model_name='teammeetingperson',
            name='meeting',
            field=models.ForeignKey(to='statscollect_db.TeamMeeting'),
        ),
        migrations.AddField(
            model_name='teammeeting',
            name='away_team',
            field=models.ForeignKey(to='statscollect_db.Team', related_name='meetings_away'),
        ),
        migrations.AddField(
            model_name='teammeeting',
            name='home_team',
            field=models.ForeignKey(to='statscollect_db.Team', related_name='meetings_home'),
        ),
        migrations.AddField(
            model_name='teammeeting',
            name='participants',
            field=models.ManyToManyField(blank=True, through='statscollect_db.TeamMeetingPerson', to='statscollect_db.Person'),
        ),
        migrations.AddField(
            model_name='footballpersonalstats',
            name='meeting',
            field=models.ForeignKey(to='statscollect_db.TeamMeeting'),
        ),
        migrations.CreateModel(
            name='FootballMeeting',
            fields=[
            ],
            options={
                'verbose_name_plural': 'rencontres (football)',
                'proxy': True,
                'verbose_name': 'rencontre (football)',
            },
            bases=('statscollect_db.teammeeting',),
        ),
    ]
