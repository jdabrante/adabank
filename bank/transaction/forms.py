from django import forms


class PaymentForm(forms.Form):
    business = forms.CharField()
    ccc = forms.CharField()
    pin = forms.CharField(widget=forms.PasswordInput)
    amount = forms.DecimalField(decimal_places=2, max_digits=10)
