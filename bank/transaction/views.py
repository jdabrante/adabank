import csv
import io
import json

import requests
from account.models import Account, Card, Status

# from weasyprint import HTML, CSS ERROR!!!!
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from xhtml2pdf import pisa

from .forms import transferOutcomingForm
from .models import Transaction, WhitelistedBank
from .utils import calc_commission

# TODO
# Refact: create a global fuction to reduce the duplicate code


@require_POST
@csrf_exempt
def payment(request: HttpRequest):
    data = json.loads(request.body)
    commission = calc_commission(Transaction.Type.PAYMENT.value, data['amount'])
    try:
        card = Card.objects.get(code=data['ccc'])
        account_balance = float(card.account.balance)
    except Card.DoesNotExist:
        return HttpResponseBadRequest(f'The card with code {data["ccc"]} does not exist')
    if not check_password(data['pin'], card.pin):
        return HttpResponseForbidden("The pin doesn't code")
    if float(data['amount']) + commission > account_balance:
        return HttpResponseBadRequest('Not enough money on account')
    if card.account.status != Status.ACTIVE:
        return HttpResponseBadRequest('Unable to use account')
    if card.status != Status.ACTIVE:
        return HttpResponseBadRequest('Unable to use card')
    concept = f'Card payment to {data["business"]}'
    card.account.balance = account_balance - (float(data['amount']) + commission)
    card.account.save()
    Transaction.objects.create(
        agent=data['business'],
        concept=concept,
        amount=data['amount'],
        kind=Transaction.Type.PAYMENT,
        card=card,
        account=card.account,
        commission=commission,
        balance=card.account.balance,
    )
    return HttpResponse()


@require_POST
@csrf_exempt
def transfer_incoming(request: HttpRequest):
    data = json.loads(request.body)
    try:
        account = Account.objects.get(code=data['cac'])
        account_balance = float(account.balance)
    except Account.DoesNotExist:
        return HttpResponseForbidden("The account doesn't code or not exist")
    if account.status != Status.ACTIVE:
        return HttpResponseBadRequest('Unable to use account')
    concept = f'Transfer received in respect of {data["concept"]}'
    commission = calc_commission(Transaction.Type.INCOMING.value, data['amount'])
    account.balance = account_balance + (float(data['amount']) - commission)
    account.save()
    Transaction.objects.create(
        agent=data['sender'],
        concept=concept,
        amount=data['amount'],
        kind=Transaction.Type.INCOMING,
        account=account,
        commission=commission,
        balance=account.balance,
    )
    return HttpResponse()


@login_required
@csrf_exempt
def transfer_outcoming(request: HttpRequest, account_id: int):
    form = transferOutcomingForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            sender_account = Account.objects.get(id=account_id)
            if sender_account.status != Status.ACTIVE:
                messages.error(
                    request,
                    _("Yo can't make transactios with this account because it's not active"),
                )
                return render(request, 'transaction/outcoming.html', dict(form=form))
            commission = calc_commission(Transaction.Type.OUTCOMING.value, cd['amount'])
            account_balance = float(sender_account.balance)
            if account_balance < float(cd['amount']) + commission:
                messages.error(request, _('Not enough money in account!'))
                return render(request, 'transaction/outcoming.html', dict(form=form))
            data = {
                'sender': sender_account.code,
                'cac': cd['cac'],
                'concept': cd['concept'],
                'amount': str(cd['amount']),
            }
            code = cd['cac'][1]
            try:
                bank_url = WhitelistedBank.objects.get(id=code).url
            except:
                messages.error(request, _('The CAC %(cac)s is not valid') % {'cac': cd['cac']})
                return render(request, 'transaction/outcoming.html', dict(form=form))
            try:
                r = requests.post(
                    bank_url,
                    json=data,
                )
            except requests.exceptions.ConnectionError:
                messages.error(
                    request,
                    _('The bank to which you are trying to make a transfer is not available.'),
                )
                return render(request, 'transaction/outcoming.html', dict(form=form))
            if r.status_code != 200:
                print(r.reason)
                messages.error(request, _('The data are not valid'))
                return render(request, 'transaction/outcoming.html', dict(form=form))
            sender_account.balance = account_balance - (float(cd['amount']) + commission)
            sender_account.save()
            new_transaction = Transaction.objects.create(
                agent=sender_account.code,
                concept=cd['concept'],
                amount=cd['amount'],
                kind=Transaction.Type.OUTCOMING,
                account=sender_account,
                commission=commission,
                balance=sender_account.balance,
            )
            return redirect('adabank:outcoming_done', transaction_id=new_transaction.pk)
        else:
            messages.error(request, _('The data are not valid'))
    return render(request, 'transaction/outcoming.html', dict(form=form))


def outcoming_done(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'transaction/outcoming_done.html', {'transaction': transaction})


def transaction_pdf(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    template = get_template('transaction/pdf.html')
    context = {'transaction': transaction}
    html_content = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=transaction_{transaction_id}.pdf'
    buffer = io.BytesIO()
    pisa.CreatePDF(html_content, dest=buffer)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required
def transactions_to_csv(request, account_id: int = None) -> HttpResponse:
    transactions = Transaction.objects.filter(account__id=account_id)
    account = Account.objects.get(id=account_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment;filename={account.code}_transactions.csv'
    writer = csv.writer(response)
    headers = [field.name for field in Transaction._meta.get_fields()]
    writer.writerow(headers)
    for transaction in transactions:
        data = []
        for header in headers:
            if (transaction.kind == 'PAY' or transaction.kind == 'OUT') and header == 'amount':
                data.append(f'-{transaction.amount}')
                continue
            elif transaction.kind == 'INC' and header == 'amount':
                data.append(f'+{transaction.amount}')
                continue
            data.append(getattr(transaction, header))
        writer.writerow(data)
    return response
