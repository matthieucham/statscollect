from rest_framework import serializers
from statscollect_db.models import RatingSource


class RatingSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingSource
        fields = ('uuid', 'name', 'website', 'field', 'type', 'country')

