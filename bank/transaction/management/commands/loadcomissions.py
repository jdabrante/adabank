from django.core.management.base import BaseCommand

from transaction.models import Commission

COMISSIONS = [
    {'kind': 'INC', 'range1': 1.00, 'range2': 2.00, 'range3': 3.00},
    {'kind': 'OUT', 'range1': 2.00, 'range2': 4.00, 'range3': 6.00},
    {'kind': 'PAY', 'range1': 2.00, 'range2': 4.00, 'range3': 6.00},
]


class Command(BaseCommand):
    help = 'Load commissions data'

    def handle(self, *args, **options):
        for comission in COMISSIONS:
            Commission.objects.create(**comission)
