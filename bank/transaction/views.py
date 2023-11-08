from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render

from account.models import Card

from .forms import PaymentForm
from .models import Transaction


@login_required
def payment(request: HttpRequest):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                card = Card.objects.get(code=cd['ccc'])
                account_balance = float(card.account.balance)
                if cd['amount'] > account_balance:
                    return HttpResponseBadRequest('Not enough money on account')
                if not check_password(cd['pin'], card.pin):
                    return HttpResponseForbidden('The pin doesn\'t match')
                concept = f'Card payment to {cd["business"]}'
                Transaction.objects.create(
                    agent=cd['business'],
                    concept=concept,
                    amount=cd['amount'],
                    kind=Transaction.Type.PAYMENT,
                    trans_method=card,
                )
                card.account.balance -= cd['amount']
                card.account.save()
                return HttpResponse(status=200)
            except Card.DoesNotExist:
                return HttpResponseBadRequest(f'The card with code {cd["ccc"]} does not exist')
    else:
        form = PaymentForm()
    return render(request, 'test.html', {'form': form})


# Transaction incoming
# Transaction outcoming
# Bank taxes
