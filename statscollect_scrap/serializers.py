from rest_framework import serializers

from .models import ScrapedDataSheet, ScrapedTeamWithPlayer
from statscollect_db import models


class ScrapedDataSheetSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=models.RatingSource.objects.all())
    match_date = serializers.DateTimeField(format='iso-8601')
    content = serializers.JSONField()

    class Meta:
        model = ScrapedDataSheet
        fields = ('hash_url', 'created_at', 'updated_at', 'source', 'content', 'match_date')


class ScrapedTeamWithPlayerSerializer(serializers.ModelSerializer):
    content = serializers.JSONField()

    class Meta:
        model = ScrapedTeamWithPlayer
        fields = ('team_name', 'created_at', 'updated_at', 'content')
