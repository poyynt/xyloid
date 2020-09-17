import random

def create_shortlink():
	chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ234567890"
	return "".join([random.choice(chars) for i in range(8)])
