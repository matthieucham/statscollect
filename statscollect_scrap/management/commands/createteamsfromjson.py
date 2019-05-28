from django.core.management.base import BaseCommand, CommandError
from statscollect_scrap.models import ScrapedTeamWithPlayer
from statscollect_db.models import Team, FootballPerson
import datetime


class Command(BaseCommand):
    help = 'Crée les équipes et les joueuses (forcément féminines) à partir des données json en bdd'

    def handle(self, *args, **options):
        for scraped in ScrapedTeamWithPlayer.objects.all():
            self.stdout.write('Import de %s ' % scraped.team_name)
            t = Team.objects.create(
                name='%s (F)' % scraped.team_name,
                short_name=scraped.team_name,
                field='FOOTBALL',

            )
            pjson = scraped.content.get('players')
            for pl in pjson:
                player = self._create_player(pl)
                t.current_members.add(player)
            t.save()

            self.stdout.write(self.style.SUCCESS('Import terminé'))

    def _create_player(self, pl):
        j = FootballPerson.objects.create(
            last_name=pl.get('last_name'),
            first_name=pl.get('first_name', ''),
            usual_name=pl.get('surname', ''),
            birth=datetime.datetime.strptime(pl.get('dob'), '%Y-%m-%d'),
            sex='F',
            field='FOOTBALL',
            position=pl.get('position')
        )
        return j
