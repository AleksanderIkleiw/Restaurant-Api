from hashlib import sha256
import os


def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()


def generate_random_hash():
    return sha256(os.urandom(32)).hexdigest()
