from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render

from account.models import Card, Account
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .forms import transferOutcomingForm


@require_POST
@csrf_exempt
def payment(request: HttpRequest):
    data = json.loads(request.body)
    try:
        card = Card.objects.get(code=data["ccc"])
        account_balance = float(card.account.balance)
    except Card.DoesNotExist:
        return HttpResponseBadRequest(
            f'The card with code {data["ccc"]} does not exist'
        )
    if not check_password(data["pin"], card.pin):
        return HttpResponseForbidden("The pin doesn't match")
    if float(data["amount"]) > account_balance:
        return HttpResponseBadRequest("Not enough money on account")
    concept = f'Card payment to {data["business"]}'
    card.account.balance = account_balance - float(data["amount"])
    card.account.save()
    Transaction.objects.create(
        agent=data["business"],
        concept=concept,
        amount=data["amount"],
        kind=Transaction.Type.PAYMENT,
        card=card,
        account=card.account,
    )
    return HttpResponse()


# curl -X POST -d '{"business": "Dulcería Dorado", "ccc": "C1-0001", "pin": "R8K", "amount": "7"}' http://127.0.0.1:8000/adabank/payment/


@require_POST
@csrf_exempt
def transfer_incoming(request: HttpRequest):
    data = json.loads(request.body)
    try:
        account = Account.objects.get(code=data["cac"])
        account_balance = float(account.balance)
    except account.DoesNotExist:
        return HttpResponseForbidden("The account doesn't match or not exist")
    concept = f'Transfer received in respect of {data["concept"]}'
    account.balance = account_balance + float(data["amount"])
    account.save()
    Transaction.objects.create(
        agent=data["sender"],
        concept=concept,
        amount=data["amount"],
        kind=Transaction.Type.INCOMING,
        account=account,
    )
    return HttpResponse()


# curl -X POST -d '{"sender": "Sabadell", "cac": "A4-0001", "concept": "Regalo", "amount": "70000"}' http://127.0.0.1:8000/adabank/transfer_incoming/


@csrf_exempt
def transfer_outcoming(request: HttpRequest):
    # if request.method == "POST":
    # form=

    try:
        account = Account.objects.get(code=data["cac"])
        account_balance = float(account.balance)
    except account.DoesNotExist:
        return HttpResponseForbidden("The account doesn't match or not exist")
    concept = f'Transfer output in respect of {data["concept"]}'
    account.balance = account_balance - float(data["amount"])
    account.save()
    Transaction.objects.create(
        agent=data["sender"],
        concept=concept,
        amount=data["amount"],
        kind=Transaction.Type.OUTCOMING,
        account=account,
    )
    return HttpResponse()


# curl -X POST -d '{"sender": "Sabadell", "cac": "A4-0001", "concept": "Regalo", "amount": "1000"}' http://127.0.0.1:8000/adabank/transfer_outcoming/
