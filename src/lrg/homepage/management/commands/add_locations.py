from django.core.management.base import BaseCommand
from homepage.models import Location
import geonamescache

class Command(BaseCommand):
    help = 'Populate the database with location data'

    def handle(self, *args, **kwargs):

        help = 'Populate the database with location data'
       
        gc = geonamescache.GeonamesCache()
        countries: dict = gc.get_countries()
        cities: dict = gc.get_cities()
        states: dict = gc.get_us_states()

        country_isos = {iso:obj['name'] for iso, obj in countries.items()}
        region_isos = {iso:obj['name'] for iso, obj in states.items()}

        self.stdout.write('Adding countries... ', ending='')
        Location.objects.bulk_create(
            [
                Location(
                    country=obj['name'],
                    country_short=iso,
                ) for iso, obj in countries.items()
            ]
        )
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Adding US States... ', ending='')
        Location.objects.bulk_create(
            [
                Location(
                    region=obj['name'],
                    region_short=code,
                    country="United States",
                    country_short="US",
                ) for code, obj in states.items()
            ]
        )
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Adding cities... ', ending='')
        Location.objects.bulk_create(
            [
                Location(
                    country=country_isos[obj.get('countrycode')] if obj.get('countrycode') in country_isos.keys() else None,
                    country_short=obj.get('countrycode') if obj.get('countrycode') in country_isos.keys() else None,
                    region=region_isos[obj.get('admin1code')] if obj.get('admin1code') in region_isos.keys() else None,
                    region_short=obj.get('admin1code') if obj.get('admin1code') in region_isos.keys() else None,
                    city=obj['name'],
                ) for _, obj in cities.items() if obj['population'] > 250000
            ]
        )
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write(self.style.SUCCESS('Location data populated.'))