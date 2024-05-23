import os
import json
from django.core.management.base import BaseCommand, CommandError
from api.models import Country, State, City

class Command(BaseCommand):
    help = 'Load city, state, and country data from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='The path to the JSON file containing the data'
        )

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        
        if not os.path.exists(json_file):
            raise CommandError(f"File '{json_file}' does not exist")

        with open(json_file, "r", encoding="utf-8") as file:
            database = json.load(file)

        for data in database:
            # Creating or getting the Country
            country, created = Country.objects.get_or_create(
                name=data["country"],
                defaults={
                    "code": data["country_code"],
                    "phone_code": data["phone_code"],
                    "nationality": data["nationality"]
                }
            )

            # Creating or getting the State
            state, created = State.objects.get_or_create(
                name=data["state"],
                defaults={
                    "code": data["state_code"],
                    "country": country
                }
            )

            # Creating the City
            city = City.objects.create(
                name=data["city"],
                state=state
            )

            self.stdout.write(self.style.SUCCESS(f"City {city.name} added to the database."))
