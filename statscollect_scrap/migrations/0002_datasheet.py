# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 14:24
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('statscollect_db', '__first__'),
        ('statscollect_scrap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedDataSheet',
            fields=[
                ('hash_url', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField()),
                ('match_date', models.DateTimeField(editable=False, null=True)),
                ('source', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='statscollect_db.RatingSource')),
            ],
            options={
                'ordering': ['-match_date'],
            },
        ),
    ]
