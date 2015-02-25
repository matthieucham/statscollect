# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statscollect_db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentinstance',
            name='status',
            field=models.CharField(default='ARCHIVED', choices=[('ONGOING', 'Ongoing'), ('ARCHIVED', 'Archived')], max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='goals_assists',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='goals_conceded',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='goals_saved',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='goals_scored',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='own_goals',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='penalties_awarded',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='penalties_scored',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='footballpersonalstats',
            name='playtime',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='tournament_instance',
            field=models.ForeignKey(related_name='meetings', to='statscollect_db.TournamentInstance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='tournament_step',
            field=models.ForeignKey(to='statscollect_db.TournamentInstanceStep', related_name='meetings', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rating',
            name='original_rating',
            field=models.DecimalField(max_digits=5, decimal_places=2, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tournamentinstancestep',
            name='tournament_instance',
            field=models.ForeignKey(related_name='steps', to='statscollect_db.TournamentInstance'),
            preserve_default=True,
        ),
    ]
