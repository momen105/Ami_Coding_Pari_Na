import jwt
import requests
from cryptography.fernet import Fernet
from django.conf import settings


def create_token(payload: dict):
    return jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.SIMPLE_JWT["ALGORITHM"],
    )


def encode(data: str):
    key = bytes(settings.SECRET_KEY, "utf-8")
    return Fernet(key).encrypt(bytes(data, "utf-8"))


def decode(token: bytes):
    key = bytes(settings.SECRET_KEY, "utf-8")
    return Fernet(key).decrypt(token).decode("utf-8")