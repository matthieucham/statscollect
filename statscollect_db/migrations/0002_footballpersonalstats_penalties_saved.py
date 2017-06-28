# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statscollect_db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='footballpersonalstats',
            name='penalties_saved',
            field=models.SmallIntegerField(null=True, blank=True),
        ),
    ]
