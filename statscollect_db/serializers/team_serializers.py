from rest_framework import serializers
from statscollect_db.models import Team
from .person_serializers import FootballPlayerSerializer
from .expandable import ExpandableSerializer


class FootballTeamSerializer(ExpandableSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballteam-detail', lookup_field='uuid')
    members = FootballPlayerSerializer(source='current_members', many=True, required=False)

    expand = ['members', ]

    class Meta:
        model = Team
        lookup_field = 'uuid',
        fields = ('uuid', 'created_at', 'updated_at', 'href', 'name', 'short_name', 'members')
