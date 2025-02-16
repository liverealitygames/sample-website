from django.urls import path

from . import views

urlpatterns = [
    path("", views.browse, name="index"),
    path("create/", views.create, name="create"),
    path("<int:community_id>/", views.community_info, name="community_info"),
    path("<int:community_id>/seasons/<int:season_id>", views.season_info, name="season_info"),
]