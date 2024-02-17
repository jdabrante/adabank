from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from transaction.models import Transaction

from .forms import AccountEditForm, CardEditForm
from .models import Account, Card, Status
from .utils import cvv_generator, expiry_generator, get_random_name, pin_generator


@login_required
def create_account(request: HttpRequest) -> HttpResponse:
    new_account = Account.objects.create(client=request.user)
    new_account.code = f'A4-{new_account.id:04d}'
    new_account.alias = get_random_name() + ' account'
    new_account.save()
    messages.success(
        request, _('The account %(new_account)s was created') % {'new_account': new_account.code}
    )
    return redirect('account:account_list')


@login_required
def create_account_confirmation(request: HttpRequest) -> HttpResponse:
    return render(request, 'account/create_confirmation.html')


@login_required
def account_list(request: HttpRequest) -> HttpResponse:
    accounts = Account.objects.filter(client=request.user, status=Status.ACTIVE)
    user_accounts = request.user.accounts.values_list('id', flat=True)
    transactions = Transaction.objects.filter(account_id__in=user_accounts)[:5]
    return render(
        request,
        'account/list.html',
        dict(accounts=accounts, transactions=transactions, section='accounts'),
    )


@login_required
def account_detail(request: HttpRequest, account_id: int) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account_id=account_id)[:10]
    return render(
        request,
        'account/detail.html',
        dict(account=account, transactions=transactions),
    )


@login_required
def card_create(request: HttpRequest, account_id: int) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    new_card = Card(
        account=account,
        expiry=expiry_generator(),
        cvv=cvv_generator(),
    )
    pin = pin_generator()
    new_card.pin = make_password(pin)
    new_card.save()
    new_card.code = f'C4-{new_card.id:04d}'
    new_card.save()
    subject = _('Pin for your new card of account %(account_code)s') % {
        'account_code': account.code
    }
    message = _(
        'Dear %(user)s\nThis is your PIN for the new requested card: %(card)s\nNEVER FORGET IT, IT WILL ONLY BE SHOWN NOW'
    ) % {'user': request.user.username, 'card': pin}
    send_mail(subject, message, 'adalovelacebank@gmail.com', [request.user.email])
    messages.success(
        request, _('The card %(card_alias)s was created') % {'card_alias': new_card.alias}
    )
    return redirect('account:card_list')


@login_required
def create_card_confirmation(request: HttpRequest, account_id: int) -> HttpResponse:
    account = Account.objects.get(id=account_id)
    return render(request, 'account/card/create_confirmation.html', dict(account=account))


@login_required
def card_list(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values_list('id', flat=True)
    cards = Card.objects.filter(account_id__in=user_accounts)
    return render(request, 'account/card/list.html', dict(cards=cards, section='cards'))


@login_required
def card_request(request: HttpRequest) -> HttpResponse:
    accounts = request.user.accounts.all()
    if not accounts:
        messages.error(request, _('You have no accounts, create one first'))
        return redirect('account:account_list')
    return render(request, 'account/card/request.html', dict(accounts=accounts))


@login_required
def card_detail(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'account/card/detail.html', dict(card=card))


@login_required
def change_status_card(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    card.status = Status.BLOCKED if card.status == Status.ACTIVE else Status.ACTIVE
    card.save()
    if card.status == Status.BLOCKED:
        messages.success(
            request, _('The card %(card_alias)s was blocked') % {'card_alias': card.alias}
        )
    else:
        messages.success(
            request, _('The card %(card_alias)s was unlocked') % {'card_alias': card.alias}
        )
    return redirect('account:card_list')


@login_required
def edit_account(request: HttpRequest, account_id: int) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    if request.method == 'POST':
        form = AccountEditForm(instance=account, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Changes done'))
            return redirect(account.get_absolute_url())
    else:
        form = AccountEditForm(instance=account)
    return render(request, 'account/edit.html', dict(form=form))


@login_required
def edit_card(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    if request.method == 'POST':
        form = CardEditForm(instance=card, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Changes done'))
            return redirect('account:card_list')
    else:
        form = CardEditForm(instance=card)
    return render(request, 'account/card/edit.html', dict(form=form))


@login_required
def delete_account_confirmation(request: HttpRequest, account_id: int) -> HttpResponse:
    account = Account.objects.get(id=account_id)
    return render(request, 'account/delete_confirmation.html', dict(account=account))


@login_required
def delete_account(request: HttpRequest, account_id) -> HttpResponse:
    account = get_object_or_404(Account, id=account_id)
    account.delete()
    return redirect('account:account_list')


@login_required
def delete_card(request: HttpRequest, card_id: int) -> HttpResponse:
    card = get_object_or_404(Card, id=card_id)
    card.delete()
    messages.success(request, _('The card %(card_alias)s was delete') % {'card_alias': card.alias})
    return redirect('account:card_list')


@login_required
def delete_card_confirmation(request: HttpRequest, card_id: int):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'account/card/delete_confirmation.html', dict(card=card))


@login_required
def transaction_list(request: HttpRequest, account_id: int = None) -> HttpResponse:
    if account_id:
        transaction_list = Transaction.objects.filter(account_id=account_id)
    else:
        user_accounts = request.user.accounts.values_list('id', flat=True)
        transaction_list = Transaction.objects.filter(account_id__in=user_accounts)
    paginator = Paginator(transaction_list, 10)
    page_num = request.GET.get('page', 1)
    transactions = paginator.page(page_num)
    return render(request, 'account/transactions/list.html', dict(transactions=transactions))
