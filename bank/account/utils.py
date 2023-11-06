import random
import string


def pin_generator() -> str:
    string_pin = string.digits + string.ascii_uppercase
    return f"{random.choice(string_pin)}{random.choice(string_pin)}{random.choice(string_pin)}"
