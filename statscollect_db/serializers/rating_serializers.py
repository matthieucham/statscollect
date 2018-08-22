from rest_framework import serializers
from statscollect_db.models import RatingSource


class RatingSourceSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    def get_country(self, obj):
        return obj.country.code

    class Meta:
        model = RatingSource
        fields = ('code', 'name', 'website', 'field', 'type', 'country',)
