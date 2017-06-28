# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statscollect_scrap', '0007_processedgamesheetplayer_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='processedgamesheetplayer',
            name='penalties_saved',
            field=models.SmallIntegerField(default=0, help_text='Nombre de pénaltys arrêtés'),
        ),
    ]
