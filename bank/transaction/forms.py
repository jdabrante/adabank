from django import forms
from django.utils.translation import gettext_lazy as _


class transferOutcomingForm(forms.Form):
    # sender = forms.CharField(label=_('sender'))
    cac = forms.CharField(label=_('cac'))
    concept = forms.CharField(label=_('concept'))
    amount = forms.DecimalField(label=_('amount'))
