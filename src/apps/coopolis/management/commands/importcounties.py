import json
from urllib.request import urlopen

from django.core.management.base import BaseCommand

from apps.coopolis.models.general import County


class Command(BaseCommand):
    help = "Imports Counties"
    counties_source = "https://analisi.transparenciacatalunya.cat/resource/gsjn-sema.json"

    def handle(self, *args, **options):
        self.import_counties()

    def import_counties(self):
        counties = json.loads(urlopen(self.counties_source).read())
        County.objects.all().delete()
        for county in counties:
            obj = County.objects.create(
                id=int(county["codi"]),
                name=county["nom"],
            )
            print(f"Creada comarca: {obj.name}")
