import random
import string
from django.utils import timezone


def pin_generator() -> str:
    string_pin = string.digits + string.ascii_uppercase
    return f"{random.choice(string_pin)}{random.choice(string_pin)}{random.choice(string_pin)}"


def cvv_generator() -> str:
    return f"{random.choice(string.digits)}{random.choice(string.digits)}{random.choice(string.digits)}"


def expiry_generator() -> str:
    return timezone.now() + timezone.timedelta(days=365 * 5)
