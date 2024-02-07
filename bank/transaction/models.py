from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Account, Card


class Transaction(models.Model):
    class Type(models.TextChoices):
        PAYMENT = 'PAY', _('Payment')
        INCOMING = 'INC', _('Incoming')
        OUTCOMING = 'OUT', _('Outcoming')

    agent = models.CharField(_('agent'), max_length=200)
    concept = models.CharField(_('concept'), max_length=50)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    kind = models.CharField(_('kind'), max_length=3, choices=Type.choices)
    account = models.ForeignKey(
        _('account'), Account, related_name='transactions', on_delete=models.CASCADE
    )
    card = models.ForeignKey(
        _('card'),
        Card,
        related_name='transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    commission = models.DecimalField(_('comission'), max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]

    def __str__(self):
        return f'{self.kind}, {self.agent}, {self.concept}'


class Commission(models.Model):
    kind = models.CharField(_('kind'), max_length=3, choices=Transaction.Type.choices)
    range1 = models.DecimalField(_('range 1'), max_digits=5, decimal_places=2)
    range2 = models.DecimalField(_('range 2'), max_digits=5, decimal_places=2)
    range3 = models.DecimalField(_('range 3'), max_digits=5, decimal_places=2)


class WhitelistedBank(models.Model):
    name = models.CharField(_('name'), max_length=20)
    url = models.CharField(max_length=250)
    code = models.CharField(_('code'), max_length=2)
