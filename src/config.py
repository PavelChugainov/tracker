from pathlib import Path

from pydantic import BaseModel, BaseS

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RSA256"
    expire_minutes: int = 3600


auth_jwt_settings = AuthJWT()
