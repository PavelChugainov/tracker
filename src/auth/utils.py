from datetime import timedelta, datetime

import jwt
from pwdlib import PasswordHash

from src.config import auth_jwt_settings

# private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."


password_hash = PasswordHash.recommended()


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt_settings.private_key_path.read_text(),
    algorithm: str = auth_jwt_settings.algorithm,
    expire_minutes: int = auth_jwt_settings.expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt_settings.public_key_path.read_text(),
    algorithm: str = auth_jwt_settings.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
):
    return password_hash.hash(password)


def validate_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)
