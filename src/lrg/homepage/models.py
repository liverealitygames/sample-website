from django.db import models

class Stamped(models.Model):

    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Editable(Stamped):

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ExternalImage(models.Model):
    
    full_size_url = models.CharField()

    class Meta:
        abstract = True


class ProfilePicture(ExternalImage):

    icon_url = models.CharField()


class User(Stamped):

    account_statuses = [
        "Active",
        "Banned",
        "Suspended",
        "Muted",
    ]

    auth_sources = [
        "Internal",  # Made an account owned by LRG with email/password
    ]

    account_status = models.CharField(choices=account_statuses)
    display_name = models.CharField(max_length=20, unique=True)
    profile_picture = models.ForeignKey(ProfilePicture, on_delete=models.CASCADE, blank=True, null=True)
    auth_source = models.CharField(choices=auth_sources)

    class Meta:
        abstract = True


class Admin(User):
    pass

