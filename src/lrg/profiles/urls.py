from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:display_name>", views.view, name="view"),
    path("<str:profile_id>/edit", views.edit, name="edit"),
]