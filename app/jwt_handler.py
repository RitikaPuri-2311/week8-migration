from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    payload = data.copy()

    payload["iat"] = datetime.utcnow()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=30)
    payload["type"] = "access"

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None