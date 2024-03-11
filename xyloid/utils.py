import random


def create_shortlink():
    chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ234567890"
    return "".join([random.choice(chars) for _ in range(8)])
