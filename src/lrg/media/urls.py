from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("podcasts", views.podcasts, name="podcasts"),
    path("news", views.news, name="news"),
]