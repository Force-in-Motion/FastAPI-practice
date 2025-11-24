from pydantic import BaseModel
from pathlib import Path

JWT_DIR = Path(__file__).parent



class JWTSettings(BaseModel):
    """Определяет пути к файлам, содержащим публичный и привытный ключи"""

    private_key: Path = JWT_DIR / "keys" / "private.pem"

    public_key: Path = JWT_DIR / "keys" / "public.pem"

    algorithm: str = "RS256"

    access_token_expire: int = 15 # Срок действия токена в минутах

    refresh_token_expire: int = 60 * 24 * 30 # Срок действия токена в минутах ( на месяц )

    access_name = 'access'

    refresh_name = 'refresh'


jwt_settings = JWTSettings()