# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-27 15:41
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('statscollect_scrap', '0009_auto_20170905_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedTeamWithPlayer',
            fields=[
                ('team_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'ordering': ['team_name'],
            },
        ),
    ]
