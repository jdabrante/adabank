from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    ACTIVE = 'ACT', _('Active')
    BLOCKED = 'BLK', _('Blocked')
    DISABLED = 'DIS', _('Disabled')


class Account(models.Model):
    client = models.ForeignKey(
        _('client'), settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts'
    )
    code = models.CharField(_('code'), max_length=7, unique=True)
    alias = models.CharField(_('alias'), max_length=250, blank=True, default='Adabank Account')
    status = models.CharField(
        _('status'), max_length=3, choices=Status.choices, default=Status.ACTIVE
    )
    balance = models.DecimalField(_('balance'), decimal_places=2, max_digits=100, default=100)

    # TODO Cambiar índices
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.alias or self.code

    def get_absolute_url(self):
        return reverse('account:account_detail', args=[self.id])


class Card(models.Model):
    account = models.ForeignKey(
        _('account'), Account, on_delete=models.CASCADE, related_name='cards'
    )
    code = models.CharField(_('code'), max_length=7, unique=True)
    alias = models.CharField(_('alias'), max_length=250, default='Adabank Card', blank=True)
    status = models.CharField(
        _('status'), max_length=3, choices=Status.choices, default=Status.ACTIVE
    )
    pin = models.CharField(_('pin'), max_length=3)
    cvv = models.CharField(max_length=3)
    expiry = models.DateTimeField(_('expiry'))

    class Meta:
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('account:card_detail', args=[self.id])
