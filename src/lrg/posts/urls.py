from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("create/", views.create, name="create"),
    path("<int:post_id>", views.info, name="info"),
    path("search", views.search, name="search"),
    path('get-cities', views.get_cities, name='get_cities'),
]