import secrets
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Status(models.TextChoices):
    ACTIVE = "ACT", "Active"
    BLOCKED = "BLK", "Blocked"
    DISABLED = "DIS", "Disabled"


class Account(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    code = models.CharField(max_length=7, unique=True)
    alias = models.CharField(max_length=250, blank=True, default="Adabank Account")
    status = models.CharField(
        max_length=3, choices=Status.choices, default=Status.ACTIVE
    )
    balance = models.DecimalField(decimal_places=2, max_digits=100, default=100)

    # TODO Cambiar índices
    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.alias or self.code

    def get_absolute_url(self):
        return reverse("account:account_detail", args=[self.id])


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cards")
    code = models.CharField(max_length=7, unique=True)
    alias = models.CharField(max_length=250, default="Adabank Card", blank=True)
    status = models.CharField(
        max_length=3, choices=Status.choices, default=Status.ACTIVE
    )
    pin = models.CharField(max_length=3)
    cvv = models.CharField(max_length=3)
    expiry = models.DateTimeField()

    class Meta:
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("account:card_detail", args=[self.id])
