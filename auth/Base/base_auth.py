import secrets
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response
from fastapi.security import HTTPBasicCredentials, HTTPBasic


router = APIRouter(tags=["Base"])

security = HTTPBasic()


# Аутентификация по HTTPBasic
@router.get("/base", response_model=dict)
async def base_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """
    Базовая утентификация при помощи HTTPBasic
    :param credentionals: объект HTTPBasicCredentials, полученный в случае успешной проверки данных классом HTTPBasic
    :return: dict
    """
    return {
        "username": credentials.username,
        "password": credentials.password,
    }


# ======================= Аутентификация по HTTPBasic ============================


user_data_auth = {
    "admin": "admin",
    "sergey": "developer",
}


async def verify_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    """
    Проверяет наличие логина и пароля пользователя в словаре и их соответствие
    :param credentionals: объект HTTPBasicCredentials, полученный в случае успешной проверки данных классом HTTPBasic
    :return: dict
    """
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    # Получает пароль пользоателя по полученному его имени
    correct_password = user_data_auth.get(credentials.username)

    # Если пароль отсутствует то и имя соответственно тоже, поскольку имя пользователя не может храниться со значением пароля равным None, выбрасываем исключение
    if correct_password is None:
        raise unauthorized

    # secrets стандартная библиотека питона, проверяет соответствие полученного пароля, паролю конкретного найденного в словаре пользователя. compare_digest - пренимает 2 обязательных параметра: полученный пароль пользователя и текущий пароль, найденный в словаре, конкретного пользователя. Сравнение происходит после декодирования обоих, в этом помогает метод encode с переданным им параметром 'utf-8', это формат, в который нужно декодировать пароль
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthorized

    # Если все проверки пройдены, то возвращаем пользователя
    return credentials.username


@router.get("/user", response_model=dict)
async def user_auth_credentials(
    user_name: str = Depends(
        verify_credentials
    ),  # При помощи зависимости получаем имя пользователя, уже прошедшего аутентификацию
) -> Dict[str, str]:
    """
    Базовая утентификация при помощи HTTPBasic, с проверкой существования в словаре полученного пользователя
    :param credentionals: объект HTTPBasicCredentials, полученный в случае успешной проверки данных классом HTTPBasic
    :return: dict
    """
    return {"username": f"Hi, {user_name}"}


# ================== Аутентификация по статическому токену ======================


auth_by_static_token = {
    "as8d79as8d798asd78asd9as7d9": "admin",
    "z87xc687zx6c876zx87c6zx87c8": "Sergey",
}


async def verify_by_static_token(
    static_token: str = Header(alias="user-static-token"),
) -> str:
    """
    Проверяет соответствие в словаре полученного токена,
    :param static_token:  alias добавляет в заголовок запроса строку с названием токена как ключ  "user-static-token" и его значение сам токен
    :return: Имя пользователя
    """
    if static_token not in auth_by_static_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return auth_by_static_token.get(static_token)


@router.get("/static-token", response_model=dict)
async def http_header_auth(
    user_name: str = Depends(
        verify_by_static_token
    ),  # При помощи зависимости получаем токен, уже уже найденный в словаре, то есть он точно существует
):
    """
    Базовая утентификация при помощи статичного токена (созданного нами в словаре), который получаем из Header (заголовка запроса)
    :param credentionals: объект HTTPBasicCredentials, полученный в случае успешной проверки данных классом HTTPBasic
    :return: dict
    """
    return {"username": f"Hi, {user_name}"}




# security = HTTPBasic() — создаётся объект, который при использовании как зависимость будет: смотреть заголовок Authorization, парсить Basic, декодировать base64 и вернуть HTTPBasicCredentials (имя + пароль в виде pydantic модели). Если заголовок отсутствует или он неверный, зависимость по умолчанию возвращает 401 с WWW-Authenticate: Basic (то есть браузер/клиент увидит приглашение ввести логин/пароль).

# В аргументе функции credentionals: Annotated[HTTPBasicCredentials, Depends(security)]:

# Depends(security) — говорит FastAPI: перед выполнением обработчика вызови зависимость security (наш HTTPBasic()).

# HTTPBasic() прочитает Authorization заголовок, декодирует Basic base64(user:pass) → вернёт HTTPBasicCredentials с полями .username и .password.

# Annotated[...] используется, чтобы совмещать тип и зависимость в одном объявлении (альтернативно можно писать credentionals: HTTPBasicCredentials = Depends(security)).



