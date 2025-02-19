from django.core.management.base import BaseCommand
from homepage.models import Location
import geonamescache



# class Command(BaseCommand):
#     help = 'Populate the database with location data'

#     def handle(self, *args, **kwargs):

#         help = 'Populate the database with location data'
       
#         gc = geonamescache.GeonamesCache()
#         countries: dict = gc.get_countries()
#         cities: dict = gc.get_cities()
#         states: dict = gc.get_us_states()

#         self.stdout.write('Adding countries... ', ending='')
#         Country.objects.bulk_create(
#             [
#                 Country(
#                     code=iso,
#                     name=obj['name']
#                 ) for iso, obj in countries.items()
#             ]
#         )
#         self.stdout.write(self.style.SUCCESS('OK'))

#         self.stdout.write('Adding US States... ', ending='')
#         usa = Country.objects.get(code='US')
#         Region.objects.bulk_create(
#             [
#                 Region(
#                     code=code,
#                     name=obj['name'],
#                     country=usa,
#                 ) for code, obj in states.items()
#             ]
#         )
#         self.stdout.write(self.style.SUCCESS('OK'))

#         self.stdout.write('Adding cities... ', ending='')
#         us_cities = {city:obj for city, obj in cities.items() if obj.get('countrycode') == 'US'} 
#         big_cities = {city:obj for city, obj in us_cities.items() if obj.get('population') > 100000}     
#         City.objects.bulk_create(
#             [
#                 City(
#                     country=Country.objects.filter(code=obj.get('countrycode')).first() if obj.get('countrycode') else None,
#                     region=Region.objects.filter(code=obj.get('admin1code')).first() if obj.get('admin1code') else None,
#                     name=obj['name'],
#                 ) for _, obj in list(big_cities.items())[:50]
#             ]
#         )
#         self.stdout.write(self.style.SUCCESS('OK'))

#         self.stdout.write('Adding Location objects... ', ending='')
#         Location.objects.bulk_create(
#             [
#                 Location(
#                     country=country
#                 ) for country in Country.objects.all()
#             ] + [
#                 Location(
#                     country=region.country,
#                     region=region
#                 ) for region in Region.objects.all()
#             ] + [
#                 Location(
#                     country=city.country,
#                     region=city.region if city.region else None,
#                     city=city
#                 ) for city in City.objects.all()
#             ]
#         )
#         self.stdout.write(self.style.SUCCESS('OK'))

#         self.stdout.write(self.style.SUCCESS('Location data populated.'))

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