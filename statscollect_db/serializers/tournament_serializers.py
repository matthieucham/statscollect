from rest_framework import serializers

from statscollect_db.models import Tournament, TournamentInstance, TournamentInstanceStep


class TournamentSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    href = serializers.HyperlinkedIdentityField(view_name='tournament-detail', lookup_field='uuid')

    def get_country(self, obj):
        if obj.country:
            return obj.country.name
        else:
            return None

    class Meta:
        model = Tournament
        fields = ('uuid', 'href', 'name', 'field', 'type', 'country')
