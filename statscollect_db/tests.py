import datetime

from django.test import TestCase

from .models import FootballPerson, Rating, Tournament, TournamentInstance, FootballMeeting, \
    FootballTeam, RatingSource, \
    TeamMeetingPerson, FootballPersonalStats


class MergePersonTest(TestCase):

    def setUp(self):
        tournament = Tournament.objects.create(name='TNMT', field='FOOTBALL', type='INT')
        instance = TournamentInstance.objects.create(tournament=tournament, name='INSTANCE')
        self.team_a = FootballTeam.objects.create(name='Team A', short_name='A', field='FOOTBALL')
        self.team_b = FootballTeam.objects.create(name='Team B', short_name='B', field='FOOTBALL')
        self.meeting = FootballMeeting.objects.create(home_team=self.team_a, away_team=self.team_b,
                                                      tournament_instance=instance, date=datetime.datetime.utcnow())

        self.fpsource = FootballPerson.objects.create(last_name='SOURCE', position='G')
        self.fptarget = FootballPerson.objects.create(last_name='TARGET', position='G')

        TeamMeetingPerson.objects.create(meeting=self.meeting, person=self.fpsource, played_for=self.team_a)

        FootballPersonalStats.objects.create(person=self.fpsource, meeting=self.meeting, playtime=90)

        self.rating = Rating.objects.create(
            person=self.fpsource,
            meeting=self.meeting,
            source=RatingSource.objects.create(code='TEST', name='TEST'),
            original_rating=5.5
        )

    def test_merge(self):
        FootballPerson.objects.merge(self.fpsource, self.fptarget)
        self.rating.refresh_from_db()
        self.assertEqual(self.fptarget.uuid, self.rating.person.uuid)
        self.meeting.refresh_from_db()
        self.assertEqual(0, self.meeting.participants.filter(uuid=self.fpsource.uuid).count())
        self.assertEqual(1, self.meeting.participants.filter(uuid=self.fptarget.uuid).count())
        self.assertEqual(0, FootballPersonalStats.objects.filter(person_id=self.fpsource.id).count())
        self.assertEqual(1, FootballPersonalStats.objects.filter(person_id=self.fptarget.id).count())
