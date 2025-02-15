from django.db import models
from homepage.models import User, Stamped, ExternalImage
from community.const import COMMUNITY_STATUSES

# Create your models here.

class Community(Stamped):



    description = models.TextField()
    organizers = models.ManyToManyField(User)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(COMMUNITY_STATUSES)
    wiki_link = models.CharField()