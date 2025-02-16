from django.db import models
from django.contrib.auth.models import User
from homepage.const import *
from datetime import datetime, timezone

class SafeGet(models.Model):
   
   def safe_get(key, value):
    try:
        val = SafeGet.objects.get(key=value)
    except SafeGet.DoesNotExist:
        val = None
    return val

class Stamped(models.Model):

    creation_time = models.DateTimeField(auto_now_add=True)

    def get_age_in_days(self): 
        return (datetime.now(timezone.utc) - self.creation_time).days
    
    def get_age(self):
        now = datetime.now(timezone.utc)
        then = self.creation_time
        age = now-then
        if int(age.days):
            if age.days > 365:
                return f"{age.days // 365} years"
            if age.days > 30:
                return f"~{age.days // 30} months"
            return f"{age.days} days"
        if int(age.seconds):
            if age.seconds > 60:
                return f"{age.seconds // 60} minutes"
            return f"{age.seconds} seconds"
        return f"less than a second"


    class Meta:
        abstract = True

class Editable(Stamped):

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ExternalImage(models.Model):
    
    full_size_url = models.CharField()
    description = models.CharField(blank=True, null=True)

    def resize(self):
        pass

    def __str__(self):
        return self.description
    

# Locations
class Country(models.Model):

    code = models.CharField(unique=True)
    name = models.CharField()

    def __str__(self):
        return self.name


class Region(models.Model):

    code = models.CharField()
    name = models.CharField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.country:
            return f"{self.name}, {self.country.code}"
        return self.name


class City(models.Model):

    name = models.CharField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.country:
            if self.region:
                return f"{self.name}, {self.region.code}, {self.country.code}"
            return f"{self.name}, {self.country.name}"
        return self.name
    

class Location(models.Model):

    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.city:
            return str(self.city)
        if self.region:
            return str(self.region)
        if self.country:
            return str(self.country)
        return "N/A"

# Profiles - more info than a user
class Profile(Stamped):

    account_status_choices = {choice:choice for choice in ACCOUNT_STATUSES}
    auth_source_choices = {choice:choice for choice in AUTH_SOURCES}

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_status = models.CharField(choices=account_status_choices)
    display_name = models.CharField(max_length=20, unique=True)
    auth_source = models.CharField(choices=auth_source_choices)
    pronouns = models.CharField(blank=True, null=True)
    icon = models.OneToOneField(ExternalImage, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.display_name
