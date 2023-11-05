from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ProfileRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label='Date of birth', widget=forms.SelectDateWidget(years=range(1900, 2200))
    )

    class Meta:
        model = Profile
        fields = ['identification']

    # def clean_identification(self):
    #     id = self.cleaned_data["identification"]
    #     if Profile.objects.filter(identification=id).exists():
    #         raise forms.ValidationError("The identification already exists")
    #     return id


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "avatar"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
