from django.urls import include, path

from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("sidebar/", views.sidebar, name="sidebar"),
]
