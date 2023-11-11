import re

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.models import Account, Card

from .forms import transferOutcomingForm
from .models import Transaction, WhitelistedBank
from .utils import calc_commission


# TODO
# Refact: create a global fuction to reduce the duplicate code


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
        return HttpResponseForbidden("The pin doesn't code")
    if float(data["amount"]) > account_balance:
        return HttpResponseBadRequest("Not enough money on account")
    concept = f'Card payment to {data["business"]}'
    commission = calc_commission(Transaction.Type.PAYMENT.value, data["amount"])
    card.account.balance = account_balance - (float(data["amount"]) + commission)
    card.account.save()
    Transaction.objects.create(
        agent=data["business"],
        concept=concept,
        amount=data["amount"],
        kind=Transaction.Type.PAYMENT,
        card=card,
        account=card.account,
        commission=commission,
    )
    return HttpResponse()


@require_POST
@csrf_exempt
def transfer_incoming(request: HttpRequest):
    data = json.loads(request.body)
    try:
        account = Account.objects.get(code=data["cac"])
        account_balance = float(account.balance)
    except Account.DoesNotExist:
        return HttpResponseForbidden("The account doesn't code or not exist")
    concept = f'Transfer received in respect of {data["concept"]}'
    commission = calc_commission(Transaction.Type.INCOMING.value, data["amount"])
    account.balance = account_balance + (float(data["amount"]) - commission)
    account.save()
    Transaction.objects.create(
        agent=data["sender"],
        concept=concept,
        amount=data["amount"],
        kind=Transaction.Type.INCOMING,
        account=account,
        commission=commission,
    )
    return HttpResponse()


@login_required
@csrf_exempt
def transfer_outcoming(request: HttpRequest, account_id: int):
    if request.method == "POST":
        form = transferOutcomingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sender_account = Account.objects.get(id=account_id)
            account_balance = float(sender_account.balance)
            if account_balance < cd["amount"]:
                messages.error(request, "Not enough money on account")
                form = transferOutcomingForm()
                return render(request, "transaction/outcoming.html", dict(form=form))
            data = {
                "sender": cd["sender"],
                "cac": cd["cac"],
                "concept": cd["concept"],
                "amount": str(cd["amount"]),
            }
            r = requests.post(
                bank_url,
                json=data,
            )
            regex = r"([A-Z]+\d+)-\d+"
            code = re.match(regex, cd["cac"]).group(1)
            bank_url = WhitelistedBank.objects.get(code=code).url
            if r.status_code != 200:
                messages.error(request, "Something went wrong with the transfer")
                form = transferOutcomingForm()
                return render(request, "transaction/outcoming.html", dict(form=form))
            commission = calc_commission(
                Transaction.Type.OUTCOMING.value, data["amount"]
            )
            sender_account.balance = account_balance - (
                float(cd["amount"]) + commission
            )
            sender_account.save()
            Transaction.objects.create(
                agent=sender_account.code,
                concept=cd["concept"],
                amount=cd["amount"],
                kind=Transaction.Type.OUTCOMING,
                account=sender_account,
                commission=commission,
            )
            return HttpResponse("Todo fue ok mi rey")
    else:
        form = transferOutcomingForm()
    return render(request, "transaction/outcoming.html", dict(form=form))


# curl -X POST -d '{"business": "Dulcería Dorado", "ccc": "C1-0001", "pin": "R8K", "amount": "7"}' http://127.0.0.1:8000/adabank/payment/
# curl -X POST -d '{"sender": "Sabadell", "cac": "A4-0001", "concept": "Regalo", "amount": "1000"}' http://127.0.0.1:8000/adabank/transfer_outcoming/
# curl -X POST -d '{"sender": "Sabadell", "cac": "A4-0001", "concept": "Regalo", "amount": "70000"}' http://127.0.0.1:8000/adabank/incoming/
