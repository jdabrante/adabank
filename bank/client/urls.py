from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("edit/", views.edit, name="edit"),
    path("sidebar/", views.sidebar, name="sidebar"),
    path("", include("django.contrib.auth.urls")),
]
