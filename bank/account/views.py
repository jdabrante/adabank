from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .forms import AccountCreationForm, CardCreationForm
from .models import Account, Card
from .utils import pin_generator


@login_required
def create_account(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        account_form = AccountCreationForm(request.POST)
        if account_form.is_valid():
            cd = account_form.cleaned_data
            if request.user.check_password(cd['password']):
                new_account = Account.objects.create(client=request.user, alias=cd['alias'])
                new_account.code = f'A4-{new_account.id:04d}'
                new_account.save()
                # El create_done se tiene que cambiar
                return render(request, 'account/create_done.html', {'new_account': new_account})
    account_form = AccountCreationForm()
    return render(request, 'account/create.html', {'account_form': account_form})

@login_required
def account_list(request:HttpRequest) -> HttpResponse:
    accounts = Account.objects.filter(client=request.user)
    return render(request, 'account/list.html', {'accounts': accounts})

@login_required
def account_detail(request:HttpRequest, account_id) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    return render(request, 'account/detail.html', {'account': account})

@login_required
def card_create(request: HttpRequest, account_id:int) -> HttpResponse:
    if request.method == 'POST':
        card_form = CardCreationForm(request.POST)
        if card_form.is_valid():
            cd = card_form.cleaned_data
            if request.user.check_password(cd['password']):
                related_account = Account.objects.get(id=account_id)
                new_card = Card.objects.create(account=related_account, alias=cd['alias'], pin=pin_generator())
                new_card.code = f'C4-{new_card.id:04d}'
                new_card.save()
                return render(request, 'account/card/create_done.html', {'new_card': new_card})
    card_form = CardCreationForm()
    return render(request, 'account/card/create_card.html', {'card_form': card_form})
