from rest_framework import serializers
from rest_framework.reverse import reverse

from statscollect_db.models import Tournament, TournamentInstance, TournamentInstanceStep


class TournamentSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    href = serializers.HyperlinkedIdentityField(view_name='tournament-detail', lookup_field='uuid')
    links = serializers.SerializerMethodField()

    def get_country(self, obj):
        if obj.country:
            return obj.country.name
        else:
            return None

    def get_links(self, obj):
        request = self.context.get('request', None)
        return {
            'instances': {
                'href': reverse(
                    'tournament-instance-list-nested', args=(obj.uuid,), request=request
                ),
            },
        }

    class Meta:
        model = Tournament
        fields = ('uuid', 'href', 'name', 'field', 'type', 'country', 'links')


class TournamentInstanceSerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='instance-detail', lookup_field='uuid')
    tournament = serializers.SlugRelatedField(slug_field='uuid', read_only=True)

    class Meta:
        model = TournamentInstance
        fields = ('uuid', 'href', 'tournament', 'name', 'start', 'end')