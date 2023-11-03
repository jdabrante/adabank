from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import (ProfileEditForm, ProfileRegistrationForm, UserEditForm,
                    UserRegistrationForm)
from .models import Profile

# TO DO
# dict(user_form=user_form, user=user)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'client/dashboard.html')


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)  # Username, first_name...
        profile_form = ProfileRegistrationForm(request.POST)  # Date birth, dni
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            # Cleaned data: {'username': dimas98, 'email': dimas@dimas.com...}
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(
                user=new_user,
                date_of_birth=profile_form.cleaned_data['date_of_birth'],
                identification=profile_form.cleaned_data['identification'],
            )
            return render(
                request,
                'client/register_done.html',
                {'new_user': new_user, 'profile_form': profile_form},
            )
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(
        request, 'client/register.html', {'user_form': user_form, 'profile_form': profile_form}
    )


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.success(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request, 'client/edit.html', {'user_form': user_form, 'profile_form': profile_form}
    )
