from django.db import models
from homepage.models import Editable, ExternalImage
from community.models import Season
from posts.const import *


class Post(Editable):
    '''
    Contains information about the Reality Game Season.
    '''

    description = models.TextField()
    season = models.OneToOneField(Season, on_delete=models.CASCADE)
    banner = models.OneToOneField(ExternalImage, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.season)
