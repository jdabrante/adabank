import json
import requests
import io
# from weasyprint import HTML, CSS ERROR!!!!
from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.pdfgen import canvas
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.models import Account, Card, Status

from .forms import transferOutcomingForm
from .models import Transaction, WhitelistedBank
from .utils import calc_commission
from django.contrib.admin.views.decorators import staff_member_required

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
    if card.account.status != Status.ACTIVE:
        return HttpResponseBadRequest("Unable to use account")
    if card.status != Status.ACTIVE:
        return HttpResponseBadRequest("Unable to use card")
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
    if account.status != Status.ACTIVE:
        return HttpResponseBadRequest("Unable to use account")
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
    form = transferOutcomingForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            cd = form.cleaned_data
            sender_account = Account.objects.get(id=account_id)
            if sender_account.status != Status.ACTIVE:
                return HttpResponseBadRequest("The account cannot be used!")
            commission = calc_commission(Transaction.Type.OUTCOMING.value, cd["amount"])
            account_balance = float(sender_account.balance)
            if account_balance < float(cd["amount"]) + commission:
                messages.error(request, "Not enough money in account!")
                form = transferOutcomingForm()
                return render(request, "transaction/outcoming.html", dict(form=form))
            data = {
                "sender": cd["sender"],
                "cac": cd["cac"],
                "concept": cd["concept"],
                "amount": str(cd["amount"]),
            }
            code = cd["cac"][1]
            bank_url = WhitelistedBank.objects.get(id=code).url
            r = requests.post(
                bank_url,
                json=data,
            )
            # if r.status_code != 200:
            #     messages.error(request, "Something went wrong with the transfer!")
            #     form = transferOutcomingForm()
            #     print(r.status_code)
            #     return render(request, "transaction/outcoming.html", dict(form=form))
            sender_account.balance = account_balance - (float(cd["amount"]) + commission)
            sender_account.save()
            new_transaction = Transaction.objects.create(
                agent=sender_account.code,
                concept=cd["concept"],
                amount=cd["amount"],
                kind=Transaction.Type.OUTCOMING,
                account=sender_account,
                commission=commission,
            )
            # return HttpResponse("Transfer done!")
            return redirect("adabank:outcoming_done", transaction_id=new_transaction.pk)
    return render(request, "transaction/outcoming.html", dict(form=form))

def outcoming_done(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, "transaction/outcoming_done.html", {"transaction": transaction})

def transaction_pdf(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    template = get_template("transaction/pdf.html")
    context = {"transaction": transaction}
    html_content = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=transaction_{transaction_id}.pdf'
    buffer = io.BytesIO()
    pisa.CreatePDF(html_content, dest=buffer)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response