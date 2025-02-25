from django.db import models
from homepage.models import Editable, ExternalImage, Location
from profiles.models import Profile
from community.const import *

# Create your models here.


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

    name = models.CharField(unique=True, max_length=256)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="communities_owned")
    status = models.CharField(choices=community_status_choices, max_length=256)
    banner = models.OneToOneField(ExternalImage, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "communities"

class ContactInfo(Editable):

    wiki = models.CharField(blank=True, null=True, max_length=256)
    instagram = models.CharField(blank=True, null=True, max_length=256)
    facebook = models.CharField(blank=True, null=True, max_length=256)
    other_link = models.CharField(blank=True, null=True, max_length=256)
    youtube = models.CharField(blank=True, null=True, max_length=256)
    community = models.OneToOneField(Community, on_delete=models.CASCADE, blank=True, null=True)

    def handle_to_link(base, handle_or_link):
        if handle_or_link[0] == "@":
            return {base:f"https://{base}.com/{handle_or_link[1:]}"}
        else:
            return {base:handle_or_link}

    def get_links(self):
        links = {}
        if self.wiki:
            links.update({"wiki":self.wiki})
        if self.instagram:
            links.update(ContactInfo.handle_to_link("instagram",self.instagram))
        if self.facebook:
            links.update(ContactInfo.handle_to_link("facebook",self.facebook))
        if self.youtube:
            links.update(ContactInfo.handle_to_link("youtube",self.youtube))
        if self.other_link:
            links.update({"other":self.other_link})
        return links
    
class Season(Editable):
    '''
    Represents a specific season attributable to a Community.
    '''

    game_format_choices = {choice:choice for choice in GAME_FORMATS}
    season_status_choices = {choice:choice for choice in SEASON_STATUSES}

    name = models.CharField(blank=True, null=True, max_length=256)
    number = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=season_status_choices, max_length=256)
    filmed = models.BooleanField(blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    application_link = models.CharField(blank=True, null=True, max_length=256)
    cast = models.ManyToManyField(Profile, related_name="seasons_as_cast")
    format = models.CharField(choices=game_format_choices, max_length=256)
    banner = models.OneToOneField(ExternalImage, on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{str(self.community)} - {self.get_name()}"
    
    def get_name(self):
        return self.name or self.format+' Season '+str(self.number)
    
    def get_start_date(self):
        return self.schedule.start_time_specific or self.schedule.start_time_range_earliest
    
    def describe(self):
        if self.description:
            return self.description
        description = ""
        description += "Game Runners: "+" / ".join([str(profile) for profile in self.community.staff.all()])+"\n"
        description += "Cast: "+" / ".join([str(profile) for profile in self.cast.all()])+"\n"
        description += "Location: "+(str(self.location) if self.location else "???")+"\n"
        description += "Schedule: "+(str(self.schedule) if self.schedule else "???")
        return description

class Staff(Editable):

    '''
    This represents both active and archived staff information. If a Staff is associated with a community,
    the assumption is that the information is current; if it is associated with a season, the assumption is that
    the information is kept for archival purposes and is not necessarily up-to-date.
    '''

    hosts = models.ManyToManyField(Profile, related_name="staff_as_host")
    contacts = models.ManyToManyField(Profile, related_name="staff_as_contact")
    general = models.ManyToManyField(Profile, related_name="staff_as_general")
    community = models.OneToOneField(Community, on_delete=models.CASCADE)

    def get_all(self):
        return list(set(self.hosts.all() + self.contacts.all() + self.general.all()))
    
    # def is_active(self):
    #     return bool(self.community)
    
    # def __str__(self):
    #     if self.is_active():
    #         return f"{self.community} (Active)"
    #     return f"{self.season} (Historical)"
