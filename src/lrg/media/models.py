from django.db import models
from homepage.models import Editable, Stamped
from media.const import *
# Create your models here.
# Podcasts to display

class Podcast(Editable):

    podcast_source_choices = {choice:choice for choice in PODCAST_SOURCES}

    title = models.CharField(max_length=256)
    embed = models.CharField(max_length=256)
    source = models.CharField(choices=podcast_source_choices, max_length=256)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    

# News articles
class Article(Stamped):

    title = models.CharField(max_length=256)
    embed = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title