import random

def create_shortlink():
    chars = "abcdefghijklmnopqrstuvwxyz"
    chars += chars.upper()
    chars += "1234567890"
    return "".join([random.choice(chars) for i in range(16)])
