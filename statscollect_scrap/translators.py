from statscollect_scrap.models import ScrappedFootballStep, ScrappedGameSheet
from statscollect_db.models import FootballMeeting, TournamentInstanceStep, TeamMeetingPerson, Team


class ScrappedFootballStepTranslator():
    """
    Translates a ScrappedFootballGameResult to a FootballMeeting entity
    """

    def translate(self, scrapped):
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
        else:
            print('Not completed yet.')


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
            #self.prepare_related(scrapped.actual_step)
        else:
            print('Not completed yet.')