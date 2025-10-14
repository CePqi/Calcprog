import jwt
from app.config import settings


def encoded_func(data, key: bytes = settings.PRIVATE_KEY, algorithm: str = settings.ALGORITHM):
    token = jwt.encode(payload=data, key=key, algorithm=algorithm)
    return token


def decoded_func(
    token: str, key: bytes = settings.PUBLIC_KEY, algorithm: str = settings.ALGORITHM
):
    data = jwt.decode(jwt=token, key=key, algorithms=[algorithm])
    return data
