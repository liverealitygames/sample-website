from django.contrib import admin
from .models import Podcast, Article, WatchParty, Fundraiser

admin.site.register(Podcast)
admin.site.register(Article)
admin.site.register(WatchParty)
admin.site.register(Fundraiser)