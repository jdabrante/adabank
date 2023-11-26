from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import (
    ProfileEditForm,
    ProfileRegistrationForm,
    UserEditForm,
    UserRegistrationForm,
)
from .models import Profile
from transaction.models import Transaction

# TO DO
# dict(user_form=user_form, user=user)


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "client/index.html")


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            # Not saving the user on DB to encrypt password
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(
                user=new_user,
                date_of_birth=profile_form.cleaned_data["date_of_birth"],
                identification=profile_form.cleaned_data["identification"],
            )
            return redirect("login")
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(
        request,
        "client/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "client/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    profile = Profile.objects.get(user=request.user)
    return render(
        request, "client/profile.html", dict(profile=profile, section="profile")
    )


def sidebar(request: HttpRequest) -> HttpRequest:
    return render(request, "client/sidebar.html")
