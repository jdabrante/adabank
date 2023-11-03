from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import AccountCreationForm
from .models import Account


@login_required
def create_account(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        account_form = AccountCreationForm(request.POST)
        if account_form.is_valid():
            cd = account_form.cleaned_data
            if request.user.check_password(cd['password']):
                new_account = Account.objects.create(client=request.user, alias=cd['alias'])
                code_number = new_account.id
                new_account.code = f'A4-{code_number:04d}'
                new_account.save()
                # El create_done se tiene que cambiar
                return render(request, 'account/create_done.html', {'new_account': new_account})
    account_form = AccountCreationForm()
    return render(request, 'account/create.html', {'account_form': account_form})

