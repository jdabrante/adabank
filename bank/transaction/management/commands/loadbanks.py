import requests
from django.core.management.base import BaseCommand

from transaction.models import WhitelistedBank


class Command(BaseCommand):
    help = 'Load bank data'

    def handle(self, *args, **options):
        url = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/notes/files/banks.json'
        response = requests.get(url)
        banks = response.json()
        for bank in banks:
            new_bank = WhitelistedBank(**bank)
            new_bank.code = new_bank.id
            new_bank.save()
