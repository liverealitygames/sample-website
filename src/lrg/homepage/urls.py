from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.home, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
]