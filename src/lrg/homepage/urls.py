from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.home, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path('get-cities', views.get_cities, name='get_cities'),
]