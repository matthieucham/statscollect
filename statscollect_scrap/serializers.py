from rest_framework import serializers

from .models import ScrapedDataSheet
from statscollect_db import models


class ScrapedDataSheetSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=models.RatingSource.objects.all())

    class Meta:
        model = ScrapedDataSheet
        fields = ('hash_url', 'created_at', 'updated_at', 'source', 'content',)