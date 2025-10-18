# This file is responsible for signing, encoding, decoding and returning JWTs.
import time
import logging
import jwt
from decouple import config

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")


# Function returns the generated Tokens(JWTs)
def token_response(token: str):
    return {"access token": token}


# Function used for signing the JWT string
def signJWT(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": int(time.time() + 600),  # must be int for JWT spec
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        return {}
