from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from account.models import Account, Card

# Pensar si utilizar una clase TextChoices o hacer un modelo nuevo
# Preguntar por comisiones como tipo


class Transaction(models.Model):
    class Type(models.TextChoices):
        PAYMENT = "PY", "Payment"
        INCOMING = "IC", "Incoming"
        OUTCOMING = "OC", "Outcoming"

    agent = models.CharField(max_length=200)
    concept = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(max_length=2, choices=Type.choices)
    account = models.ForeignKey(
        Account, related_name="transactions", on_delete=models.CASCADE
    )
    card = models.ForeignKey(
        Card, related_name="transactions", on_delete=models.CASCADE, null=True
    )

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
        ]

    def __str__(self):
        return f"{self.kind}, {self.agent}, {self.concept}"
