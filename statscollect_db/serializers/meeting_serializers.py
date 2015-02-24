from rest_framework import serializers

from statscollect_db import models
from .team_serializers import FootballTeamSerializer
from .person_serializers import PersonSerializer
from .expandable import ExpandableSerializer


class MeetingSerializer(serializers.ModelSerializer):
    # href = serializers.HyperlinkedIdentityField(view_name='meeting-detail', lookup_field='uuid')
    tournament_instance = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    step = serializers.SlugRelatedField(slug_field='uuid', read_only=True, source='tournament_step',
                                        required=False)

    def to_representation(self, value):
        if value.teammeeting is not None:
            tournament_field = value.tournament_instance.tournament.field
            if tournament_field == 'FOOTBALL':
                tm_serial = FootballMeetingSummarySerializer(value.teammeeting, context=self.context)
                return tm_serial.to_representation(value.teammeeting)
            else:
                # TODO
                return None
        return super(MeetingSerializer, self).to_representation(value)

    class Meta:
        model = models.Meeting
        fields = (
            'uuid',
            #'href',
            'tournament_instance', 'step', 'date', )


class FootballMeetingSummarySerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballmeeting-detail', lookup_field='uuid')
    tournament_instance = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    step = serializers.SlugRelatedField(slug_field='uuid', read_only=True,
                                        source='tournament_step',
                                        required=False)
    home_team = serializers.SlugRelatedField(slug_field='name', read_only=True)
    away_team = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = models.FootballMeeting
        fields = (
            'uuid',
            'href',
            'tournament_instance', 'step', 'date', 'home_team', 'home_result', 'away_team',
            'away_result')


class FootballMeetingDetailedSerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballmeeting-detail', lookup_field='uuid')
    tournament_instance = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    step = serializers.SlugRelatedField(slug_field='uuid', read_only=True,
                                        source='tournament_step',
                                        required=False)

    home_team = FootballTeamSerializer(read_only=True)
    away_team = FootballTeamSerializer(read_only=True)

    participants = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = models.FootballMeeting
        fields = (
            'uuid',
            'href',
            'tournament_instance', 'step', 'date', 'home_team', 'home_result', 'away_team',
            'away_result', 'participants')