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
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json 


@require_POST
@csrf_exempt
def payment(request: HttpRequest):
    data = json.loads(request.body)
    try:
        card = Card.objects.get(code=data["ccc"])
        account_balance = float(card.account.balance)
        if not check_password(data["pin"], card.pin):
            return HttpResponseForbidden("The pin doesn't match")
        if float(data['amount']) > account_balance:
            return HttpResponseBadRequest("Not enough money on account")
        concept = f'Card payment to {data["business"]}'
        Transaction.objects.create(
            agent=data["business"],
            concept=concept,
            amount=data["amount"],
            kind=Transaction.Type.PAYMENT,
            card=card,
            account=card.account,
        )
        card.account.balance = account_balance - float(data["amount"])
        card.account.save()
        return HttpResponse(status=200)
    except Card.DoesNotExist:
        return HttpResponseBadRequest(f'The card with code {data["ccc"]} does not exist')


# Transaction incoming
# Transaction outcoming
# Bank taxes
