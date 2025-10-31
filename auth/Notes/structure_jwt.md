JWT — шпаргалка (для FastAPI / Python)

Кратко, всё в одном месте: структура, что означает каждая часть токена, как формируется подпись, примеры и «что передавать» в payload, рекомендации по хранению и обновлению токенов.

1. Общая структура JWT

JWT — это строка в формате:

<header>.<payload>.<signature>


где каждая часть — base64url-encoded JSON (для header и payload) или base64url байтов подписи.

Пример (три части):

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
.
eyJzdWIiOiIxMjMiLCJ1c2VybmFtZSI6ImFsaWNlIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjMwOTI0MDAwLCJleHAiOjE2MzA5Mjc2MDB9
.
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk

2. Header — что внутри и зачем

Header (заголовок) — JSON с метаданными о токене:

{
  "alg": "HS256",   // алгоритм подписи (обязательно)
  "typ": "JWT",     // тип токена (обычно JWT)
  "kid": "key1"     // (опционально) id ключа — для поиска публичного ключа в JWKS
}


alg — указывает, как вычислять/проверять подпись (HS256, RS256, ES256 и т.д.).

typ — просто информативно; чаще "JWT".

kid — полезно при асимметричной подписи и ротации ключей, чтобы получать правильный публичный ключ.

Header кодируется в base64url.

3. Payload (claims) — что это и как использовать

Payload — JSON c набором claims (утверждений). Claims бывают трёх типов:

3.1 Registered claims (стандартные, рекомендованные)

iss — issuer — кто выдал токен (строка, напр. https://auth.myapp.com).

sub — subject — идентификатор субъекта (обычно user id). Часто строка "123" или UUID.

aud — audience — кому предназначен токен (API id, клиент).

exp — expiration time — время истечения (UNIX timestamp в секундах). Токен недействителен после этого времени.

nbf — not before — токен не действителен до этого времени.

iat — issued at — время выдачи (UNIX timestamp).

jti — JWT ID — уникальный идентификатор токена (полезно для blacklist/ревокации).

3.2 Public (custom) claims

Это любые имена, согласованные между сервисами, напр. role, scope, org_id.

3.3 Private claims

Ваши внутренние поля, только для ваших сервисов.

Пример payload:

{
  "sub": "123",           // user id в вашей системе
  "username": "alice",    // дополнительная информация (несекретная)
  "role": "admin",        // права/роли
  "iat": 1732028392,      // когда выдан (UTC, seconds)
  "exp": 1732031992       // когда истекает (UTC, seconds)
}


Важно: payload не зашифрован — его можно декодировать без ключа. Не храните в payload секреты (пароли, токены доступа к 3rd-party, чувствительные PII), если только вы не шифруете токен (JWE).

4. Signature — что это и как формируется

Подпись обеспечивает целостность и подтверждает, что токен выдал тот, у кого есть ключ.

Общая формула (HS256):

signature = HMACSHA256( base64url(header) + "." + base64url(payload), SECRET_KEY )


Потом bytes подписи кодируются в base64url и добавляются как третья часть токена.

Пояснения:

base64url(header) — это header JSON, закодированный в base64url (без = padding, с - и _ вместо + и /).

base64url(payload) — аналогично для payload.

**.(точка)** — разделитель; подпись вычисляется по строкеheader.payload`.

SECRET_KEY (HS*) — общий симметричный секрет. Для асимметричных алгоритмов (RS256, ES256) используется приватный ключ для подписи, публичный — для проверки.

HMACSHA256 — конкретная хеш-функция в HS256. Для RS256 используется RSA + SHA256 (PKCS#1 v1.5), для ES256 — ECDSA.

Почему base64url?

Обычный base64 содержит символы + / и = (padding). В JWT используется variant без padding и с URL-safe символами (- и _) — чтоб безопасно передавать в URL/заголовках.

5. Пример пошагового формирования подписи (HS256)

Header JSON:

{"alg":"HS256","typ":"JWT"}


→ base64url(header) → eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

Payload JSON:

{"sub":"123","username":"alice","role":"admin","iat":1732028392,"exp":1732031992}


→ base64url(payload) → eyJzdWIiOiIxMjMiLCJ1c2VybmFtZSI6ImFsaWNlIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzMyMDI4Mzk...

Соединяем:

message = base64url(header) + "." + base64url(payload)


Подписываем:

signature_bytes = HMAC_SHA256(SECRET_KEY, message)
signature = base64url(signature_bytes)


Итог JWT:

<base64url(header)>.<base64url(payload)>.<base64url(signature)>

6. Проверка JWT (verify) — что сервер делает

При получении токена сервер должен:

Разбить строку по . → header_enc, payload_enc, signature_enc.

Декодировать header и payload (base64url → JSON) — НЕ доверять полям, нужно проверить подпись.

Восстановить message = header_enc + "." + payload_enc.

В зависимости от alg:

HS*: вычислить HMAC(message, SECRET) и сравнить с signature.

RS*/ES*: использовать публичный ключ и крипто-валидацию подписи.

Проверить exp (и nbf, iat) — убедиться, что токен не просрочен и уже действителен.

Проверить iss и aud (если используются) — защититься от токенов, предназначенных для других сервисов.

(Опционально) Проверить jti против blacklist/DB, если есть ревокация.

Важно: сравнение подписи должно быть временнно-стойким (constant-time), чтобы предотвратить тайминг-атаки. Библиотеки обычно это делают.

7. Алгоритмы и когда их применять

HS256 / HS512 — симметричный (секрет). Подходит, когда и подпись, и проверка выполняются в одном доверенном сервисе.

RS256 / ES256 — асимметричные. Подписывает приватный ключ (Auth server), проверяет публичный (resource servers). Хорошо для микросервисов и публичных валидаторов.

alg = none — НЕ ИСПОЛЬЗОВАТЬ (пустая подпись — уязвимость).

8. Типичные поля payload — что туда класть и зачем

sub (string): уникальный id пользователя (например "user:42" или UUID). Главное поле для идентификации субъекта.

username (string): удобно для логов/отображения, но не секрет.

role / scope (string/list): права доступа/скоупы.

iat (int): время выдачи (unix seconds).

exp (int): время окончания жизни.

jti (string): уникальный id токена (для blacklist / отслеживания).

iss / aud (string): issuer / audience.

Не хранить в payload: пароли, секреты, персональные данные, tokens к 3rd-party (если они чувствительны).

9. Refresh tokens — практический паттерн (рекомендуемый)

Access token: короткий (5–30 минут).

Refresh token: долгоживущий (дни/недели), opaque (рандомная строка) или JWT + server-side state.

Ротация refresh токенов:

При каждом POST /auth/refresh выдаётся новый refresh token, старый помечается как использованный (revoked).

Если старый token снова используется → возможен replay (компрометация) → лог아ут всех сессий или блокировка пользователя.

Хранить refresh токены на сервере (БД/Redis) с полями: token, user_id, issued_at, expires_at, revoked, device/session meta.

10. Где хранить токены (веб-клиент vs мобильный)

Browser SPA:

Access token: в памяти (не в localStorage) или в short-lived HttpOnly cookie.

Refresh token: HttpOnly, Secure cookie + SameSite (или хранить на сервере).

При использовании cookie — защититься от CSRF (double submit, SameSite, CSRF token).

Mobile / Desktop:

Использовать secure storage (Keychain/Android Keystore).

Never store tokens in plain localStorage if you expect XSS vectors.

11. Реализация в FastAPI — минимальный пример (PyJWT / python-jose)

Пример функций создания и проверки токена (используя [python-jose]):

# core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()  # загружает из env

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"iat": int(now.timestamp()), "exp": int(expire.timestamp())})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e


Использовать в route:

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    # далее fetch user из БД по user_id
    return {"id": user_id, "payload": payload}

12. Ревокация и blacklist

JWT по умолчанию stateless — нельзя отозвать подписанный токен без хранения state. Подходы:

Короткий access token — уменьшает окно компрометации.

Blacklist (store jti в Redis/DB при ревокации) — при верификации проверять, не отозван ли jti.

Token version / session id — в payload хранить session_id/token_version и сверять с БД (если версия не совпадает → токен недействителен).

13. Частые ошибки и уязвимости

Хранение long-lived token в localStorage → XSS.

Не проверять aud / iss.

Использовать alg: none или доверять client-provided alg.

Использовать один и тот же secret для access и refresh.

Не шифровать чувствительные данные в payload.

Не обрабатывать повторное использование refresh token (нет ротации).

14. Checklist для production

 HTTPS + HSTS.

 SECRET_KEY в секретном хранилище (.env + vault).

 Access token lifetime: 5–30 мин.

 Refresh tokens: rotation + server-side storage + revoke.

 Проверять exp, nbf, iss, aud.

 Использовать RS256 + JWKS, если нужен публичный верификатор.

 Логи и мониторинг повторных refresh-операций.

 Ограничение размера payload (не больше пары KB).

 CSRF защита, если используете cookie.

 Ротация ключей (key rotation) и kid в header.

15. Краткие полезные команды/функции (Python)

Кодирование header/payload в base64url:

import base64, json
def b64url_encode(obj: dict) -> str:
    raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


HMAC SHA256 (подпись):

import hmac, hashlib
def sign_hs256(message: bytes, secret: bytes) -> bytes:
    return hmac.new(secret, message, hashlib.sha256).digest()


(Это низкоуровнево — лучше использовать python-jose / PyJWT.)

16. Ещё раз — что означают примеры полей (разбор)
{
  "sub": "123",           // subject — id пользователя (ключевой идентификатор)
  "username": "alice",    // не секретная инфо для удобства
  "role": "admin",        // права пользователя (используется в проверках)
  "iat": 1732028392,      // issued at — когда выдан (unix seconds)
  "exp": 1732031992       // expiration — когда истекает (unix seconds)
}


sub — главное поле для поиска user в БД.

username — дублирующее/удобное поле, чтобы не обращаться в БД в простых случаях (но не надежно).

role — может быть строкой или массивом (например ["user","editor"]).

iat/exp — целые секунды Unix; сервер должен сравнивать с int(datetime.utcnow().timestamp()).