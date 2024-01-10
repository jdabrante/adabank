import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from .forms import AccountCreationForm, AccountEditForm, CardCreationForm, CardEditForm
from .models import Account, Card, Status
from transaction.models import Transaction
from .utils import pin_generator, cvv_generator, expiry_generator


@login_required
def create_account(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        account_form = AccountCreationForm(request.POST)
        if account_form.is_valid():
            cd = account_form.cleaned_data
            if request.user.check_password(cd["password"]):
                new_account = Account.objects.create(
                    client=request.user, alias=cd["alias"]
                )
                new_account.code = f"A4-{new_account.id:04d}"
                new_account.save()
                # El create_done se tiene que cambiar
                return redirect("account:account_list")
    account_form = AccountCreationForm()
    return render(request, "account/create.html", dict(account_form=account_form))


@login_required
def account_list(request: HttpRequest) -> HttpResponse:
    accounts = Account.objects.filter(client=request.user, status=Status.ACTIVE)
    user_accounts = request.user.accounts.values_list("id", flat=True)
    transactions = Transaction.objects.filter(account_id__in=user_accounts)[:10]
    return render(
        request,
        "account/list.html",
        dict(accounts=accounts, transactions=transactions, section="accounts"),
    )


@login_required
def account_detail(request: HttpRequest, account_id: int) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account_id=account_id)[:10]
    return render(
        request,
        "account/detail.html",
        dict(account=account, transactions=transactions),
    )


@login_required
def card_create(request: HttpRequest, account_id) -> HttpResponse:
    if request.method == "POST":
        card_form = CardCreationForm(request.POST)
        if card_form.is_valid():
            cd = card_form.cleaned_data
            if request.user.check_password(cd["password"]):
                account = get_object_or_404(Account, id=account_id)
                new_card = Card(account=account, alias=cd["alias"], expiry=expiry_generator(),cvv=cvv_generator())
                pin = pin_generator()
                new_card.pin = make_password(pin)
                new_card.save()
                new_card.code = f"C4-{new_card.id:04d}"
                new_card.save()
                return render(
                    request,
                    "account/card/create_done.html",
                    dict(new_card=new_card, pin=pin),
                )
    card_form = CardCreationForm()
    return render(request, "account/card/create_card.html", dict(card_form=card_form))


@login_required
def card_list(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values_list("id", flat=True)
    accounts = Account.objects.filter(client=request.user, status=Status.ACTIVE)
    cards = Card.objects.filter(account_id__in=user_accounts)
    return render(request, "account/card/list.html", dict(cards=cards, section="cards"))


@login_required
def card_detail(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    return render(request, "account/card/detail.html", dict(card=card))


@login_required
def change_status_card(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    card.status = Status.BLOCKED if card.status == Status.ACTIVE else Status.ACTIVE
    card.save()
    return render(
        request,
        "account/change_status.html",
        dict(
            card=card,
        ),
    )


@login_required
def edit_account(request: HttpRequest, account_id: int) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        form = AccountEditForm(instance=account, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(account.get_absolute_url())
    else:
        form = AccountEditForm(instance=account)
    return render(request, "account/edit.html", dict(form=form))


@login_required
def edit_card(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    if request.method == "POST":
        form = CardEditForm(instance=card, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(card.get_absolute_url())
    else:
        form = CardEditForm(instance=card)
    return render(request, "account/card/edit.html", dict(form=form))


# @login_required
# def disable_account(request: HttpRequest, account_id) -> HttpResponse:
#     account = get_object_or_404(Account, id=account_id)
#     account.status = Status.DISABLED
#     return redirect("account:account_list")


@login_required
def delete_account(request: HttpRequest, account_id) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    account.delete()
    return redirect("account:account_list")


@login_required
def delete_card(request: HttpRequest, card_id) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    card.delete()
    return redirect("account:card_list")


@login_required
def transaction_list(request: HttpRequest, account_id: int = None) -> HttpResponse:
    if account_id:
        transaction_list = Transaction.objects.filter(account_id=account_id)
    else:
        user_accounts = request.user.accounts.values_list("id", flat=True)
        transaction_list = Transaction.objects.filter(account_id__in=user_accounts)
    paginator = Paginator(transaction_list, 10)
    page_num = request.GET.get("page", 1)
    transactions = paginator.page(page_num)
    return render(
        request, "account/transactions/list.html", dict(transactions=transactions)
    )

@login_required
def transactions_to_csv(request, account_id: int) -> HttpResponse:
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
            data.append(getattr(transaction, header))
        writer.writerow(data)
    return response