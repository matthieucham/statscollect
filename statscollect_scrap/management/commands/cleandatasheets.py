from django.core.management.base import BaseCommand, CommandError
from statscollect_scrap.models import ScrapedDataSheet


class Command(BaseCommand):
    help = 'Purge toutes les scrappeddatasheets'

    def handle(self, *args, **options):
        ScrapedDataSheet.objects.all().delete()
        self.stdout.write("Purge done")
