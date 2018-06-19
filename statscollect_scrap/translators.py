from statscollect_db.models import FootballMeeting, TeamMeetingPerson, \
    FootballPersonalStats, Rating, AlternativePersonName


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

    def _store_alt_name(self, scraped):
        if scraped.scraped_ratio is None:
            return
        if scraped.scraped_ratio < 75 and scraped.scraped_name:
            AlternativePersonName.objects.create(person=scraped.footballperson.person_ptr, alt_name=scraped.scraped_name)

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
            self._store_alt_name(sg)
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
            tmp_obj.penalties_saved = sg.penalties_saved
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
            self._store_alt_name(sr)
