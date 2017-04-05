from rest_framework import serializers

from .models import ScrapedDataSheet


class ScrapedDataSheetSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field='code', read_only=True)

    class Meta:
        model = ScrapedDataSheet
        fields = ('hash_url', 'created_at', 'updated_at', 'source', 'content',)