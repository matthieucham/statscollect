from rest_framework import serializers
from statscollect_db.models import RatingSource


class RatingSourceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ratingsource-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = RatingSource
        fields = ('uuid', 'name', 'website', 'field', 'type', 'country', 'url')

