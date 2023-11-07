from django.contrib.contenttypes.models import ContentType

from .models import Transaction


def create_transaction(agent, concept, timestamp, amount, kind, target):
    target_ct = ContentType.objects.get_for_model(target)
