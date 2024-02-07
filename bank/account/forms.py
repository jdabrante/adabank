from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Account, Card

# Alguna manera de refactorizar esto


class AccountCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['alias']
        labels = {'alias': _('alias')}


class CardCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = Card
        fields = ['alias']
        labels = {'alias': _('alias')}


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['alias']
        labels = {'alias': _('alias')}


class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['alias']
        labels = {'alias': _('alias')}
