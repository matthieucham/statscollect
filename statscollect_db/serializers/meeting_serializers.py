from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from statscollect_db import models
from .team_serializers import FootballTeamSerializer


class MeetingSerializer(serializers.ModelSerializer):
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
            'created_at', 'updated_at',
            'tournament_instance', 'step', 'date', 'created_at', 'updated_at',)


class FootballMeetingSummarySerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballmeeting-detail', lookup_field='uuid')
    tournament_instance = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    step = serializers.SlugRelatedField(slug_field='uuid', read_only=True,
                                        source='tournament_step',
                                        required=False)
    home_team = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    away_team = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    home_team_name = serializers.SerializerMethodField()
    away_team_name = serializers.SerializerMethodField()

    def get_home_team_name(self, obj):
        return obj.home_team.__str__()

    def get_away_team_name(self, obj):
        return obj.away_team.__str__()

    class Meta:
        model = models.FootballMeeting
        fields = (
            'uuid',
            'created_at', 'updated_at',
            'href',
            'tournament_instance', 'step', 'date', 'home_team', 'home_team_name', 'home_result', 'away_team',
            'away_team_name', 'away_result')


class FootballStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FootballPersonalStats
        fields = (
            'playtime',
            'goals_scored',
            'goals_assists',
            'penalties_scored',
            'penalties_awarded',
            'goals_saved',
            'goals_conceded',
            'own_goals'
        )


class RatingSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    source_name = serializers.SlugRelatedField(source='source', slug_field='name', read_only=True)
    rating = serializers.DecimalField(decimal_places=1, max_digits=3, read_only=True, source='original_rating')

    class Meta:
        model = models.Rating
        fields = (
            # 'code',
            'source',
            'source_name',
            'rating',
        )


class RosterPlayerIdSerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballplayer-detail', lookup_field='uuid')

    class Meta:
        model = models.Person
        fields = (
            'uuid',
            'href',
            'last_name',
            'first_name',
            'usual_name',
        )


class RosterPlayerStatsField(serializers.RelatedField):
    def to_representation(self, value):
        """ value is a teammeetingperson """
        try:
            stats_entry = models.FootballPersonalStats.objects.get(meeting=value.meeting, person=value.person)
            return FootballStatsSerializer().to_representation(instance=stats_entry)
        except ObjectDoesNotExist:
            return None


class RosterPlayerSerializer(serializers.ModelSerializer):
    player = RosterPlayerIdSerializer(source='person')
    stats = serializers.SerializerMethodField(read_only=True)
    ratings = serializers.SerializerMethodField(read_only=True)
    played_for = serializers.SlugRelatedField(slug_field='uuid', read_only=True)

    def get_stats(self, obj):
        return RosterPlayerStatsField(read_only=True).to_representation(obj)

    def get_ratings(self, value):
        ratings = models.Rating.objects.filter(meeting=value.meeting, person=value.person)
        return RatingSerializer(many=True, read_only=True).to_representation(ratings)

    class Meta:
        model = models.TeamMeetingPerson
        fields = (
            'player',
            'played_for',
            'stats',
            'ratings',
        )


class FootballMeetingDetailedSerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='footballmeeting-detail', lookup_field='uuid')
    tournament_instance = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    step = serializers.SlugRelatedField(slug_field='uuid', read_only=True,
                                        source='tournament_step',
                                        required=False)
    roster = RosterPlayerSerializer(source='teammeetingperson_set', many=True, read_only=True)
    home_team = FootballTeamSerializer(read_only=True)
    away_team = FootballTeamSerializer(read_only=True)

    class Meta:
        model = models.FootballMeeting
        fields = (
            'uuid',
            'created_at', 'updated_at',
            'href',
            'tournament_instance',
            'step',
            'date',
            'home_team',
            'home_result',
            'away_team',
            'away_result',
            'roster',
        )
#
#
# class PlayedTournamentInstanceSerializer(ExpandableSerializer):
#     href = serializers.HyperlinkedIdentityField(view_name='instance-detail', lookup_field='uuid')
#     tournament = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
#     #tournament_name = serializers.SlugRelatedField(slug_field='name', read_only=True)
#     meetings = MeetingSerializer(many=True, read_only=True, required=False)
#
#     # def get_fields(self, *args, **kwargs):
#     #     fields = super(PlayedTournamentInstanceSerializer, self).get_fields(*args, **kwargs)
#     #     uuid_person = self.context['view'].kwargs['person']
#     #     try:
#     #         #player = FootballPerson.objects.select_related('teammeeting_set').get(uuid=uuid_person)
#     #         fields['meetings'].queryset = FootballMeeting.objects.filter(participants__uuid__iexact=uuid_person)
#     #     except ObjectDoesNotExist:
#     #         pass
#     #     return fields
#
#     class Meta:
#         model = TournamentInstance
#         fields = ('uuid',
#                   'href',
#                   'tournament',
#                   #'tournament_name',
#                   'name',
#                   #'steps',
#                   'meetings')