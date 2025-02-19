from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.browse, name="browse"),
    path("create/", views.create, name="create"),
    path("<int:post_id>", views.info, name="info"),
    path("search", views.search, name="search"),
    path("search/<str:query>", views.search, name="search"),
]