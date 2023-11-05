import random
import string


def pin_generator() -> str:
    random_list = string.digits + string.ascii_uppercase
    return f'{random.choice(random_list)}{random.choice(random_list)}{random.choice(random_list)}'