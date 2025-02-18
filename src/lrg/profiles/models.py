from django.db import models
from homepage.models import Editable, ExternalImage
from django.contrib.auth.models import User
from profiles.const import *


# Create your models here.
# Profiles - more info than a user
class Profile(Editable):

    account_status_choices = {choice:choice for choice in ACCOUNT_STATUSES}
    auth_source_choices = {choice:choice for choice in AUTH_SOURCES}

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_status = models.CharField(choices=account_status_choices)
    auth_source = models.CharField(choices=auth_source_choices, default="Internal")
    pronouns = models.CharField(blank=True, null=True)
    icon = models.OneToOneField(ExternalImage, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username