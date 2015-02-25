# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statscollect_db', '0002_auto_20150225_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingsource',
            name='code',
            field=models.CharField(max_length=8, default='EQ'),
            preserve_default=False,
        ),
    ]
