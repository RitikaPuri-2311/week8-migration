import hashlib

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
    
# ACCESS TOKEN (15 min)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# REFRESH TOKEN (7 days)
def create_refresh_token():
    expire = datetime.utcnow() + timedelta(days=7)

    raw_token = jwt.encode(
        {"exp": expire, "type": "refresh"},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return raw_token, expire


# HASH REFRESH TOKEN (store in DB)
def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None