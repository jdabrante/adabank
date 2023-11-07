from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Pensar si utilizar una clase TextChoices o hacer un modelo nuevo
# Preguntar por comisiones como tipo


class Transaction(models.Model):
    class Type(models.TextChoices):
        PAYMENT = 'PY', 'Payment'
        INCOMING = 'IC', 'Incoming'
        OUTCOMING = 'OC', 'Outcoming'

    target_ct = models.ForeignKey(
        ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    trans_method = GenericForeignKey('target_ct', 'target_id')
    agent = models.CharField(max_length=200)
    concept = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(max_length=2, choices=Type.choices)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['target_ct', 'target_id']),
        ]

    def __str__(self):
        return f'{self.kind}, {self.agent}, {self.concept}'
