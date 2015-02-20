from rest_framework import serializers
from statscollect_db.models import Team
from .person_serializers import PersonSerializer


class FootballTeamSerializer(serializers.HyperlinkedModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballteam-detail', lookup_field='uuid')
    member_set = PersonSerializer(source='current_members', many=True, required=False)

    class Meta:
        model = Team
        lookup_field = 'uuid',
        fields = ('uuid', 'href', 'name', 'short_name', 'member_set')
