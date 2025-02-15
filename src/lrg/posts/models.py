from django.db import models
from homepage.models import User, Stamped, ExternalImage
from community.models import Community
from posts.const import GAME_FORMATS

from geosky import geo_plug

class Season(Stamped):
    '''
    Represents a specific season attributable to an Organization.
    '''

    VALID_COUNTRIES = geo_plug.all_CountryNames() + ["Online"]

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    application_link = models.CharField(blank=True, null=True)
    staff = models.ManyToManyField(User)
    cast = models.ManyToManyField(User)
    game_format = models.CharField(choices=GAME_FORMATS)
    location = models.CharField(blank=True, null=True)
    country = models.CharField(choices=VALID_COUNTRIES)
    game_length = models.CharField(blank=True, null=True)
    contact_info = models.CharField(blank=True, null=True)
    filmed = models.BooleanField(blank=True, null=True)
    start_time = models.CharField()


class Post(Stamped):
    '''
    Contains information about the Reality Game.
    '''

    description = models.TextField()
    has_been_edited = models.BooleanField()
    image = models.ForeignKey(ExternalImage, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)


class Organizer(User):
    '''
    Has the ability to create or edit posts on behalf of an Reality Game.
    '''

    pass


class Organization(Stamped):

    ORG_STATUSES = [
        "Casting",
        "Running",
        "Hiatus",
        "Defunct",
        "Unknown",
    ]

    description = models.TextField()
    organizers = models.ManyToManyField(Organizer)
    seasons = models.ManyToManyField(Season)
    status = models.CharField(choices=ORG_STATUSES)
    wiki_link = models.CharField()
