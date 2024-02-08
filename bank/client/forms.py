from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'placeholder': _('Password')})
    )
    password2 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'placeholder': _('Re-type Password')})
    )
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Username')}),
        help_text='',
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('First Name')}),
        help_text='',
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Last Name')}),
        help_text='',
    )
    email = forms.EmailField(
        label='', widget=forms.EmailInput(attrs={'placeholder': _('Email')}), help_text=''
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_("Passwords don't match."))
        return cd['password2']


class ProfileRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='', widget=forms.TextInput(attrs={'type': 'date'}))
    identification = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': _('Identification')})
    )

    class Meta:
        model = Profile
        fields = ['identification']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'avatar']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
