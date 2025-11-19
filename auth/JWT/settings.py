from pydantic import BaseModel
from pathlib import Path

JWT_DIR = Path(__file__).parent


class JWTSettings(BaseModel):
    """ Определяет пути к файлам, содержащим публичный и привытный ключи """

    private_key: Path = JWT_DIR / 'keys' / 'jwt_private.pem'

    public_key: Path = JWT_DIR / 'keys' / 'jwt_public.pem'

    algorithm: str = 'RS256'

    access_token_expire: int = 3
    
    refresh_token_expire: int = 60

