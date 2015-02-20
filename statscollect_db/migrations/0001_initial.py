# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FootballPersonalStats',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('playtime', models.SmallIntegerField(null=True)),
                ('goals_scored', models.SmallIntegerField(null=True)),
                ('goals_assists', models.SmallIntegerField(null=True)),
                ('penalties_scored', models.SmallIntegerField(null=True)),
                ('penalties_awarded', models.SmallIntegerField(null=True)),
                ('goals_saved', models.SmallIntegerField(null=True)),
                ('goals_conceded', models.SmallIntegerField(null=True)),
                ('own_goals', models.SmallIntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('usual_name', models.CharField(max_length=50, blank=True)),
                ('birth', models.DateField(null=True, blank=True)),
                ('sex', models.CharField(default='M', max_length=1, choices=[('M', 'Male'), ('F', 'Female')])),
                ('rep_country', django_countries.fields.CountryField(max_length=2, blank=True)),
                ('field', models.CharField(max_length=10, choices=[('FOOTBALL', 'Football')])),
                ('status', models.CharField(max_length=10, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')])),
                ('migration_id', models.CharField(max_length=35, unique=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('original_rating', models.FloatField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RatingSource',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=400)),
                ('field', models.CharField(max_length=10, choices=[('FOOTBALL', 'Football')], blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2, blank=True)),
                ('type', models.CharField(default='10CLASSIC', max_length=10, choices=[('10CLASSIC', 'Classical 0-10'), ('6GERMAN', 'German 1-6')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=50)),
                ('field', models.CharField(max_length=10, choices=[('FOOTBALL', 'Football'), ('CYCLING', 'Cycling')])),
                ('country', django_countries.fields.CountryField(max_length=2, blank=True)),
                ('migration_id', models.CharField(max_length=35, unique=True, null=True)),
                ('current_members', models.ManyToManyField(related_name='current_teams', to='statscollect_db.Person', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamMeeting',
            fields=[
                ('meeting_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='statscollect_db.Meeting')),
                ('home_result', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('away_result', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('away_team', models.ForeignKey(related_name='meetings_away', to='statscollect_db.Team')),
                ('home_team', models.ForeignKey(related_name='meetings_home', to='statscollect_db.Team')),
            ],
            options={
                'abstract': False,
            },
            bases=('statscollect_db.meeting',),
        ),
        migrations.CreateModel(
            name='TeamMeetingPerson',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(to='statscollect_db.TeamMeeting')),
                ('person', models.ForeignKey(to='statscollect_db.Person')),
                ('played_for', models.ForeignKey(to='statscollect_db.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('field', models.CharField(max_length=10, choices=[('FOOTBALL', 'Football')])),
                ('type', models.CharField(max_length=3, choices=[('NAT', 'National'), ('INT', 'International')])),
                ('country', django_countries.fields.CountryField(max_length=2, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TournamentInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('tournament', models.ForeignKey(to='statscollect_db.Tournament')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TournamentInstanceStep',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.UUIDField(unique=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('tournament_instance', models.ForeignKey(to='statscollect_db.TournamentInstance')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='teammeeting',
            name='participants',
            field=models.ManyToManyField(to='statscollect_db.Person', null=True, blank=True, through='statscollect_db.TeamMeetingPerson'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rating',
            name='meeting',
            field=models.ForeignKey(to='statscollect_db.Meeting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rating',
            name='person',
            field=models.ForeignKey(to='statscollect_db.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rating',
            name='source',
            field=models.ForeignKey(to='statscollect_db.RatingSource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='tournament_instance',
            field=models.ForeignKey(to='statscollect_db.TournamentInstance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='tournament_step',
            field=models.ForeignKey(to='statscollect_db.TournamentInstanceStep', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='footballpersonalstats',
            name='meeting',
            field=models.ForeignKey(to='statscollect_db.TeamMeeting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='footballpersonalstats',
            name='person',
            field=models.ForeignKey(to='statscollect_db.Person'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='FootballMeeting',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('statscollect_db.teammeeting',),
        ),
        migrations.CreateModel(
            name='FootballPerson',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('statscollect_db.person',),
        ),
        migrations.CreateModel(
            name='FootballTeam',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('statscollect_db.team',),
        ),
    ]
