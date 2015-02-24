from rest_framework import serializers
from statscollect_db.models import Team
from .person_serializers import PersonSerializer
from .expandable import ExpandableSerializer


class FootballTeamSerializer(ExpandableSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballteam-detail', lookup_field='uuid')
    members = PersonSerializer(source='current_members', many=True, required=False)

    expand = ['members', ]

    class Meta:
        model = Team
        lookup_field = 'uuid',
        fields = ('uuid', 'href', 'name', 'short_name', 'members')
