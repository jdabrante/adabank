from django import forms

from .models import Account, Card

# Alguna manera de refactorizar esto


class AccountCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ["alias"]


class CardCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Card
        fields = ["alias"]


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["alias"]


class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["alias"]
