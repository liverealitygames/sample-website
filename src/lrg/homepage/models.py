from django.db import models
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
    
    full_size_url = models.CharField(max_length=256)
    description = models.CharField(blank=True, null=True, max_length=256)

    def resize(self):
        pass

    def __str__(self):
        return self.description
    

# Locations
class Location(models.Model):

    country = models.CharField(blank=True, null=True, max_length=256)
    country_short = models.CharField(blank=True, null=True, max_length=256)
    region = models.CharField(blank=True, null=True, max_length=256)
    region_short = models.CharField(blank=True, null=True, max_length=256)
    city = models.CharField(blank=True, null=True, max_length=256)

    def __str__(self):
        if self.city:
            if self.country:
                if self.region:
                    return f"{self.city}, {self.region_short}, {self.country_short}"
                return f"{self.city}, {self.country}"
            return self.city
        if self.region:
            if self.country:
                return f"{self.region}, {self.country_short}"
            return self.region
        if self.country:
            return str(self.country)
        return "N/A"
