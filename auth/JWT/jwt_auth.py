# Для кодирования и декодирования, а так же выпуста JWT токена и его составляющий  используется библиотека pyJWT с расширением Cryptographic
# pip install 'pyJWT[crypto]'

from auth.JWT.schemas.token import TokenSchema
from auth.JWT.schemas.user import UserPublicSchema, UserSchema
from auth.JWT.utils import JWTUtils, AuthUtils
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer


http_bearer = HTTPBearer(auto_error=False)  # В свагер добавит новое поле (для тестирования), которое будет авторизовывать пользователя через токен

router = APIRouter(
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],  # http_bearer обязательно нужно добавить в зависимость роутера, чтобы он срабатывал по умолчанию при запуске роутера
)


@router.post(
    "/login",
    response_model=TokenSchema,
)
async def issues_acces_and_refresh_jwt_to_user(
    user: UserSchema = Depends(AuthUtils.validate_user),
) -> TokenSchema:
    """
    Возвращает access_token и refresh_token в заголовке, в случае успешной аутентификации через зависимость ( Выдает токены пользователю ),
    В тело функции мы попадем только в случае успешной валидации логина и пароля
    :param user: Выполняет валидацию пользователя по всем описанным в логике сценариям, входит в тело обработчика только в случае выполнения этой зависимости
    :return: access_token и refresh_token в теле запроса
    """
    access_token = JWTUtils.create_access_token(user=user)

    refresh_token = JWTUtils.create_refresh_token(user=user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# response_model_exclude_none уберет из схемы ответа (TokenSchema) параметры, имеющие значения умолчанию  None, по скольку refresh_token по умолчанию None
# и для этого запроса на перевыпуск access_token переопределять refresh_token мы не планируем, то чтобы не возвращать в схеме None мы используем такой параметр роутера
@router.post(
    "/refresh",
    response_model=TokenSchema,
    response_model_exclude_none=True,
)
async def reissues_access_jwt_for_user(
    user: UserSchema = Depends(AuthUtils.get_current_user_by_refresh),
) -> TokenSchema:
    """
    Возвращает access_token и refresh_token в заголовке, в случае успешной аутентификации через зависимость ( Выдает токены пользователю ),
    В тело функции мы попадем только в случае успешной валидации логина и пароля
    :param user: Выполняет валидацию пользователя по refresh_token, входит в тело обработчика только в случае выполнения этой зависимости
    :return: новый access_token
    """
    access_token = JWTUtils.create_access_token(user=user)

    return TokenSchema(
        access_token=access_token,
    )


@router.get("/me", response_model=UserPublicSchema)
async def get_user_profile(
    user: UserSchema = Depends(AuthUtils.get_current_user_by_access),
) -> UserPublicSchema:
    """
    Предоставляет пользователю доступ к своим данным в случае успешной проверки данных в токене через зависимость при помощи access_token
    :param user: Выполняет валидацию пользователя по refresh_token, входит в тело обработчика только в случае выполнения этой зависимости
    :return: Пользователя
    """
    return user
