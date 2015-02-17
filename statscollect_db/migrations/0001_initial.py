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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('playtime', models.SmallIntegerField()),
                ('goals_scored', models.SmallIntegerField()),
                ('goals_assists', models.SmallIntegerField()),
                ('penalties_scored', models.SmallIntegerField()),
                ('penalties_awarded', models.SmallIntegerField()),
                ('goals_saved', models.SmallIntegerField()),
                ('goals_conceded', models.SmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('usual_name', models.CharField(blank=True, max_length=50)),
                ('birth', models.DateField(blank=True, null=True)),
                ('sex', models.CharField(default='M', max_length=1, choices=[('M', 'Male'), ('F', 'Female')])),
                ('rep_country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('field', models.CharField(max_length=10, choices=[('FOOTBALL', 'Football')])),
                ('status', models.CharField(max_length=10, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')])),
                ('migration_id', models.CharField(max_length=35, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('original_rating', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RatingSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=400)),
                ('field', models.CharField(blank=True, max_length=10, choices=[('FOOTBALL', 'Football')])),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=50)),
                ('field', models.CharField(max_length=10, choices=[('FOOTBALL', 'Football')])),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('migration_id', models.CharField(max_length=35, null=True, unique=True)),
                ('current_members', models.ManyToManyField(blank=True, related_name='current_teams', to='statscollect_db.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamMeeting',
            fields=[
                ('meeting_ptr', models.OneToOneField(to='statscollect_db.Meeting', primary_key=True, serialize=False, parent_link=True, auto_created=True)),
                ('home_result', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('away_result', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('away_team', models.ForeignKey(to='statscollect_db.Team', related_name='meetings_away')),
                ('home_team', models.ForeignKey(to='statscollect_db.Team', related_name='meetings_home')),
            ],
            options={
                'abstract': False,
            },
            bases=('statscollect_db.meeting',),
        ),
        migrations.CreateModel(
            name='TeamMeetingPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('field', models.CharField(max_length=10, choices=[('FOOTBALL', 'Football')])),
                ('type', models.CharField(max_length=3, choices=[('NAT', 'National'), ('INT', 'International')])),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TournamentInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
            field=models.ManyToManyField(to='statscollect_db.Person', through='statscollect_db.TeamMeetingPerson'),
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
            name='player',
            field=models.ForeignKey(to='statscollect_db.Person'),
            preserve_default=True,
        ),
    ]
