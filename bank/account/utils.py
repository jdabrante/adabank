import random
import string

import requests
from django.utils import timezone


def pin_generator(size=3) -> str:
    string_pin = string.digits + string.ascii_uppercase
    return f"{''.join(random.choice(string_pin) for _ in range(size))}"


def cvv_generator(size=3) -> str:
    return f"{''.join(random.choice(string.digits) for _ in range(size))}"


def expiry_generator() -> str:
    return timezone.now() + timezone.timedelta(days=365 * 5)


def get_random_name() -> str:
    cities = requests.get('https://names.sdelquin/city/')
    return random.choice(cities.json())
