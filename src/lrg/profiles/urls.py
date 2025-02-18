from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit", views.edit, name="edit"),
    path("<str:username>", views.view, name="view"),
]