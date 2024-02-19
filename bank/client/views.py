import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from account.models import Account, Card
from account.utils import cvv_generator, expiry_generator, pin_generator

from .forms import ProfileEditForm, ProfileRegistrationForm, UserEditForm, UserRegistrationForm
from .models import Profile


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'client/index.html')


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            # Not saving the user on DB to encrypt password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(
                user=new_user,
                date_of_birth=profile_form.cleaned_data['date_of_birth'],
                identification=profile_form.cleaned_data['identification'],
            )
            new_account = Account.objects.create(client=new_user)
            new_account.code = f'A4-{new_account.id:04d}'
            new_account.save()
            pin = pin_generator()
            new_card = Card(account=new_account, expiry=expiry_generator(), cvv=cvv_generator())
            new_card.pin = make_password(pin)
            new_card.save()
            new_card.code = f'C4-{new_card.id:04d}'
            new_card.save()
            subject = _('Pin for your new card of account %(account_code)s') % {
                'account_code': new_account.code
            }
            message = _(
                'Dear new client\nThis is your PIN for the new requested card: %(card)s\nNEVER FORGET IT, IT WILL ONLY BE SHOWN NOW'
            ) % {'user': request.user.username, 'card': pin}
            send_mail(subject, message, 'adalovelacebank@gmail.com', [new_user.email])
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(
        request,
        'client/register.html',
        {'user_form': user_form, 'profile_form': profile_form},
    )


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Changes done'))
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'client/edit.html',
        {'user_form': user_form, 'profile_form': profile_form},
    )


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    profile = Profile.objects.get(user=request.user)
    return render(request, 'client/profile.html', dict(profile=profile, section='profile'))


def download_pdf(request):
    html = render_to_string('test/pdf/test.html')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=test.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/test.css')]
    )
    return response
