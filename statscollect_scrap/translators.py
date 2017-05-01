from statscollect_scrap.models import ScrappedFootballStep, ScrappedGameSheet, ScrappedTeamMeetingData, \
    ScrappedTeamMeetingRatings, RatingSource
from statscollect_db.models import FootballMeeting, TournamentInstanceStep, TeamMeetingPerson, TeamMeeting, \
    FootballPersonalStats, Rating, FootballTeam


class ScrappedFootballStepTranslator():
    """
    Translates a ScrappedFootballGameResult to a FootballMeeting entity
    """

    def translate(self, scrapped, **kwargs):
        if not isinstance(scrapped, ScrappedFootballStep):
            raise TypeError('ScrappedFootballStepTranslator operates on ScrappedFootballStep '
                            'instances.')
        if scrapped.status in ['COMPLETE', 'AMENDED']:
            for sg in scrapped.scrappedfootballgameresult_set.all():
                # Find existing entity
                matching = FootballMeeting.objects.filter(tournament_step=scrapped.actual_step).filter(
                    home_team=sg.actual_home_team).filter(away_team=sg.actual_away_team)
                if len(matching) == 0:
                    meeting_obj = FootballMeeting()
                    meeting_obj.tournament_instance = scrapped.actual_step.tournament_instance
                    meeting_obj.tournament_step = scrapped.actual_step
                    meeting_obj.date = sg.actual_game_date
                    meeting_obj.home_team = sg.actual_home_team
                    meeting_obj.away_team = sg.actual_away_team
                else:
                    meeting_obj = matching[0]
                meeting_obj.home_result = sg.actual_home_score
                meeting_obj.away_result = sg.actual_away_score
                meeting_obj.save()
                if kwargs['update_names']:
                    hteam = FootballTeam.objects.get(pk=meeting_obj.home_team_id)
                    hteam.name = sg.read_home_team
                    hteam.save()

                    ateam = FootballTeam.objects.get(pk=meeting_obj.away_team_id)
                    ateam.name = sg.read_away_team
                    ateam.save()
            self.prepare_related(scrapped.actual_step)
        else:
            print('Not completed yet.')

    def prepare_related(self, step):
        """
        Creates ScrappedGameSheets.
        """
        if not isinstance(step, TournamentInstanceStep):
            raise TypeError('prepare_related operates on TournamentInstanceStep '
                            'instances.')
        for tm in step.meetings.all():
            if tm.teammeeting:
                matching = ScrappedGameSheet.objects.filter(actual_meeting=tm.teammeeting)
                if len(matching) == 0:
                    sgs = ScrappedGameSheet()
                    sgs.actual_meeting = tm.teammeeting
                    sgs.actual_instance = step.tournament_instance
                    sgs.actual_step = step
                    sgs.actual_tournament = step.tournament_instance.tournament
                else:
                    sgs = matching[0]
                sgs.save()


class ScrappedGamesheetTranslator():
    def translate(self, scrapped, update_teams=False):
        if not isinstance(scrapped, ScrappedGameSheet):
            raise TypeError('ScrappedGamesheetTranslatorTranslator operates on ScrappedGamesheetTranslator '
                            'instances.')
        if scrapped.status in ['COMPLETE', 'AMENDED']:
            for sg in scrapped.scrappedgamesheetparticipant_set.all():
                # Find existing entity
                matching = TeamMeetingPerson.objects.filter(meeting=scrapped.actual_meeting).filter(
                    person=sg.actual_player)
                if len(matching) == 0:
                    tmp_obj = TeamMeetingPerson()
                    tmp_obj.meeting = scrapped.actual_meeting
                    tmp_obj.person = sg.actual_player
                    tmp_obj.played_for_id = sg.actual_team_id
                else:
                    tmp_obj = matching[0]
                tmp_obj.save()
                # Update player current_team if requested
                if update_teams:
                    sg.actual_player.current_teams.clear()  # remove all
                    sg.actual_player.current_teams.add(sg.actual_team_id)
                    sg.save()
            self.prepare_related(scrapped.actual_meeting)
        else:
            print('Not completed yet.')

    def prepare_related(self, team_meeting):
        """
        Creates ScrappedStatistics.
        """
        if not isinstance(team_meeting, TeamMeeting):
            raise TypeError('prepare_related operates on TeamMeeting '
                            'instances.')
        matching = ScrappedTeamMeetingData.objects.filter(teammeeting=team_meeting)
        if len(matching) == 0:
            stmd = ScrappedTeamMeetingData()
            stmd.teammeeting = team_meeting
            stmd.save()

        # Research and create for each expected source
        expected_rs = RatingSource.objects.filter(
            expectedratingsource__tournament_instance=team_meeting.tournament_instance)
        for ers in expected_rs:
            existing = ScrappedTeamMeetingRatings.objects.filter(rating_source=ers).filter(
                teammeeting=team_meeting)
            if len(existing) == 0:
                stmd = ScrappedTeamMeetingRatings()
                stmd.teammeeting = team_meeting
                stmd.rating_source = ers
                stmd.save()


class ScrappedTeamMeetingDataTranslator():
    def translate(self, scrapped):
        if not (isinstance(scrapped, ScrappedTeamMeetingData)):
            raise TypeError('ScrappedTeamMeetingDataTranslator operates on ScrappedTeamMeetingData '
                            'instances.')
        if scrapped.status in ['COMPLETE', 'AMENDED']:
            for plstat in scrapped.scrappedplayerstats_set.all():
                # Find existing entity
                matching = FootballPersonalStats.objects.filter(meeting=scrapped.teammeeting).filter(
                    person=plstat.teammeetingperson.person)
                if len(matching) == 0:
                    tmp_obj = FootballPersonalStats()
                    tmp_obj.meeting = scrapped.teammeeting
                    tmp_obj.person = plstat.teammeetingperson.person
                else:
                    tmp_obj = matching[0]
                tmp_obj.goals_assists = plstat.actual_assists
                tmp_obj.goals_conceded = plstat.actual_conceded
                tmp_obj.goals_saved = plstat.actual_saves
                tmp_obj.goals_scored = plstat.actual_goals_scored
                tmp_obj.own_goals = plstat.actual_own_goals
                tmp_obj.penalties_awarded = plstat.actual_penalties_assists
                tmp_obj.penalties_scored = plstat.actual_penalties_scored
                tmp_obj.playtime = plstat.actual_playtime
                tmp_obj.save()
        else:
            print('Not completed yet.')


class ScrappedRatingsTranslator():
    def translate(self, scrapped):
        if not (isinstance(scrapped, ScrappedTeamMeetingRatings)):
            raise TypeError('ScrappedRatingsTranslator operates on ScrappedTeamMeetingRatings '
                            'instances.')
        if scrapped.status in ['COMPLETE', 'AMENDED']:
            for sr in scrapped.scrappedplayerratings_set.all():
                if sr.actual_rating is None:  # Some scrapped rating may be null, don't save them.
                    continue
                # Find existing entity
                matching = Rating.objects.filter(meeting=scrapped.teammeeting).filter(
                    person=sr.teammeetingperson.person).filter(source=scrapped.rating_source)
                if len(matching) == 0:
                    tmp_obj = Rating()
                    tmp_obj.meeting = scrapped.teammeeting
                    tmp_obj.person = sr.teammeetingperson.person
                    tmp_obj.source = scrapped.rating_source
                else:
                    tmp_obj = matching[0]
                tmp_obj.original_rating = sr.actual_rating
                tmp_obj.save()
        else:
            print('Not completed yet.')


class ProcessedGameTranslator():
    def translate(self, processedgame):
        meeting = self._process_meeting(processedgame)
        self._process_players(processedgame, meeting)
        self._process_ratings(processedgame, meeting)
        processedgame.status = 'COMPLETE'
        processedgame.save()

    def _process_meeting(self, processedgame):
        # Find existing entity
        matching = FootballMeeting.objects.filter(tournament_step=processedgame.actual_step).filter(
            home_team=processedgame.processedgamesummary.home_team).filter(
            away_team=processedgame.processedgamesummary.away_team)
        if len(matching) == 0:
            meeting_obj = FootballMeeting(tournament_instance=processedgame.actual_step.tournament_instance,
                                          tournament_step=processedgame.actual_step,
                                          date=processedgame.processedgamesummary.game_date,
                                          home_team=processedgame.processedgamesummary.home_team,
                                          away_team=processedgame.processedgamesummary.away_team)
        else:
            meeting_obj = matching[0]
        meeting_obj.home_result = processedgame.processedgamesummary.home_score
        meeting_obj.away_result = processedgame.processedgamesummary.away_score
        meeting_obj.save()
        return meeting_obj

    def _process_players(self, processedgame, meeting):
        for sg in processedgame.processedgamesheetplayer_set.all():
            # Find existing entity
            matching = TeamMeetingPerson.objects.filter(meeting=meeting).filter(
                person=sg.footballperson.person_ptr)
            if len(matching) == 0:
                tmp_obj = TeamMeetingPerson(meeting=meeting, person=sg.footballperson.person_ptr,
                                            played_for_id=sg.team.id)
            else:
                tmp_obj = matching[0]
            tmp_obj.save()
            # stats
            # Find existing entity
            matching = FootballPersonalStats.objects.filter(meeting=meeting).filter(person=sg.footballperson.person_ptr)
            if len(matching) == 0:
                tmp_obj = FootballPersonalStats(meeting=meeting, person=sg.footballperson.person_ptr)
            else:
                tmp_obj = matching[0]
            tmp_obj.goals_assists = sg.goals_assists
            tmp_obj.goals_conceded = sg.goals_conceded
            tmp_obj.goals_saved = sg.goals_saves
            tmp_obj.goals_scored = sg.goals_scored
            tmp_obj.own_goals = sg.own_goals
            tmp_obj.penalties_awarded = sg.penalties_assists
            tmp_obj.penalties_scored = sg.penalties_scored
            tmp_obj.playtime = sg.playtime
            tmp_obj.save()

    def _process_ratings(self, processedgame, meeting):
        for sr in processedgame.processedgamerating_set.all():
            if sr.rating is None:  # Some scrapped rating may be null, don't save them.
                continue
            # Find existing entity
            matching = Rating.objects.filter(meeting=meeting, person=sr.footballperson.person_ptr,
                                             source=sr.rating_source)
            if len(matching) == 0:
                tmp_obj = Rating(meeting=meeting, person=sr.footballperson.person_ptr, source=sr.rating_source)
            else:
                tmp_obj = matching[0]
            tmp_obj.original_rating = sr.rating
            tmp_obj.save()
