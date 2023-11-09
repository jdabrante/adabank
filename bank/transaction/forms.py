from django import forms


class transferOutcomingForm(forms.Form):
    sender = forms.CharField()
    cac = forms.CharField()
    concept = forms.CharField()
    amount = forms.DecimalField()

