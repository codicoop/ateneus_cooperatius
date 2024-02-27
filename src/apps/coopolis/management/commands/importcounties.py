import json
from urllib.request import urlopen

from django.core.management.base import BaseCommand

from apps.coopolis.models.general import County, Town


class Command(BaseCommand):
    help = "Imports Counties"
    counties_source = "https://analisi.transparenciacatalunya.cat/resource/gsjn-sema.json"
    towns_source = "https://analisi.transparenciacatalunya.cat/resource/9aju-tpwc.json"

    def handle(self, *args, **options):
        # Not using this one because we did it in a data migration
        # self.import_counties()
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

    def import_towns(self):
        towns = json.loads(urlopen(self.towns_source).read())
        total_matches = 0
        total_not_matched = 0
        for town in towns:
            name = town["nom"]
            if self.get_hardcoded_town(town["nom"]):
                name = self.get_hardcoded_town(town["nom"])
                print(f"Name of {town['nom']} resolved to {name}")
            if name == "Esquirol, l'":
                if not Town.objects.filter(name=name).exists():
                    # Needs to be added to databaseº
                    Town.objects.create(
                        name=name,
                        name_for_justification=name,
                        county_id=int(town["codi_comarca"]),
                    )
                continue

            res = Town.objects.filter(name__unaccent__iexact=name)
            if res:
                print(f"Matched! {len(res)} coincidències.")
                for match in res:
                    total_matches += 1
                    print(f"Matched! {town['nom']} == {match.name}")
                    match.name_for_justification = match.name
                    match.name = town["nom"]
                    match.county_id = int(town["codi_comarca"])
                    match.save()
            else:
                total_not_matched += 1
                print(f"Not matched: {town['nom']}")

        print(f"Total poblacions: {Town.objects.all().count()}")
        print(f"Total de coincidències: {total_matches}")
        print(f"Total de NO coincidències: {total_not_matched}")

    def get_hardcoded_town(self, name):
        equivalencies = {
            "Brunyola i Sant Martí Sapresa": "BRUNYOLA",
            "Calonge i Sant Antoni": "CALONGE",
            "Bigues i Riells del Fai": "BIGUES I RIELLS",
            "Ràpita, la": "SANT CARLES DE LA RAPITA",
            "Roda de Berà": "RODA DE BARA",
            "Saus, Camallera i Llampaies": "SAUS,CAMALLERA I LLAMPAIES",
        }
        return equivalencies.get(name)

    def check_towns(self):
        towns = Town.objects.all()
        path = 'apps/dataexports/fixtures/correlations_2021_2022.json'
        with open (path, 'r') as json_file:
            data_json = json.load(json_file)
        for town in towns: 
            if town.name not in data_json['towns']:
                print(f"{town} is wrong.")