# from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AccountCreationForm, AccountEditForm, CardCreationForm, CardEditForm
from .models import Account, Card, Status
from transaction.models import Transaction
from .utils import pin_generator

CARD_CHAR_ID = "C"
ACCOUNT_CHAR_ID = "A"


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
    return render(request, "account/create.html", {"account_form": account_form})


@login_required
def account_list(request: HttpRequest) -> HttpResponse:
    accounts = Account.objects.filter(client=request.user, status=Status.ACTIVE)
    transactions = Transaction.objects.all()[:10]
    return render(
        request,
        "account/list.html",
        {"accounts": accounts, "transactions": transactions},
    )


@login_required
def account_detail(request: HttpRequest, account_id: int) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    transactions = account.transactions.all()[:10]
    return render(
        request,
        "account/detail.html",
        {"account": account, "transactions": transactions},
    )


@login_required
def card_create(request: HttpRequest, account_id) -> HttpResponse:
    if request.method == "POST":
        card_form = CardCreationForm(request.POST)
        if card_form.is_valid():
            cd = card_form.cleaned_data
            if request.user.check_password(cd["password"]):
                account = get_object_or_404(Account, id=account_id)
                new_card = Card(account=account, alias=cd["alias"])
                pin = pin_generator()
                new_card.pin = make_password(pin)
                new_card.save()
                new_card.code = f"C4-{new_card.id:04d}"
                new_card.save()
                return render(
                    request,
                    "account/card/create_done.html",
                    {"new_card": new_card, "pin": pin},
                )
    card_form = CardCreationForm()
    return render(request, "account/card/create_card.html", {"card_form": card_form})


@login_required
def card_list(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values_list("id", flat=True)
    cards = Card.objects.filter(account_id__in=user_accounts)
    return render(request, "account/card/list.html", {"cards": cards})


@login_required
def card_detail(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    return render(request, "account/card/detail.html", {"card": card})


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


@login_required
def disable_account(request: HttpRequest, account_id) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    account.status = Status.DISABLED
    return redirect("account:account_list")


@login_required
def cancel_card(request: HttpRequest, card_id) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    card.delete()
    return redirect("account:card_list")


# def edit(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         user_form = UserEditForm(instance=request.user, data=request.POST)
#         profile_form = ProfileEditForm(
#             instance=request.user.profile, data=request.POST, files=request.FILES
#         )
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, "Profile updated successfully")
#         else:
#             messages.success(request, "Error updating your profile")
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = ProfileEditForm(instance=request.user.profile)
#     return render(
#         request,
#         "client/edit.html",
#         {"user_form": user_form, "profile_form": profile_form},
#     )
