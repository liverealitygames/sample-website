from django.db import models
from homepage.models import Profile, Editable, ExternalImage, Location
from community.const import *

# Create your models here.

class ContactInfo(Editable):

    wiki = models.CharField(blank=True, null=True)
    instagram = models.CharField(blank=True, null=True)
    facebook = models.CharField(blank=True, null=True)
    bluesky = models.CharField(blank=True, null=True)


class Schedule(Editable):

    game_length_range_shortest = models.IntegerField(blank=True, null=True)
    game_length_range_longest = models.IntegerField(blank=True, null=True)
    game_length_range_exact = models.IntegerField(blank=True, null=True)
    start_time_range_earliest = models.DateField(blank=True, null=True)
    start_time_range_latest = models.DateField(blank=True, null=True)
    start_time_specific = models.DateField(blank=True, null=True)

    def has_fuzzy_length(self):
        return bool(self.game_length_range_longest or self.game_length_range_longest)
    
    def has_fuzzy_start_time(self):
        return bool(self.start_time_range_earliest or self.start_time_range_latest)


class Community(Editable):

    community_status_choices = {choice:choice for choice in COMMUNITY_STATUSES}

    name = models.CharField(default="N/A")
    description = models.TextField(blank=True, null=True)
    staff = models.ManyToManyField(Profile, related_name="communities_as_staff")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="communities_owned")
    status = models.CharField(choices=community_status_choices)
    contact = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, blank=True, null=True)
    banner = models.OneToOneField(ExternalImage, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "communities"


class Season(Editable):
    '''
    Represents a specific season attributable to a Community.
    '''

    game_format_choices = {choice:choice for choice in GAME_FORMATS}
    season_status_choices = {choice:choice for choice in SEASON_STATUSES}

    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=season_status_choices)
    filmed = models.BooleanField(blank=True, null=True)
    season_name = models.CharField(blank=True, null=True)
    season_number = models.IntegerField(blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    application_link = models.CharField(blank=True, null=True)
    staff = models.ManyToManyField(Profile, related_name="seasons_as_staff")
    cast = models.ManyToManyField(Profile, related_name="seasons_as_cast")
    game_format = models.CharField(choices=game_format_choices)
    season_banner = models.OneToOneField(ExternalImage, on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{str(self.community)} - {self.get_name()}"
    
    def get_name(self):
        return self.season_name or self.game_format+' Season '+str(self.season_number)
    
    def describe(self):
        if self.description:
            return self.description
        description = ""
        description += "Game Runners: "+" / ".join([str(profile) for profile in self.staff.all()])+"\n"
        description += "Cast: "+" / ".join([str(profile) for profile in self.cast.all()])+"\n"
        description += "Location: "+(str(self.location) if self.location else "???")+"\n"
        description += "Schedule: "+(str(self.schedule) if self.schedule else "???")
        return description
