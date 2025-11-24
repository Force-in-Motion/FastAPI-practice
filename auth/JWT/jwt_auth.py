# Для кодирования и декодирования, а так же выпуста JWT токена и его составляющий  используется библиотека pyJWT с расширением Cryptographic
# pip install 'pyJWT[crypto]'

from auth.JWT.schemas.token import TokenSchema
from auth.JWT.schemas.user import UserPublicSchema, UserSchema
from auth.JWT.utils import JWTUtils, AuthUtils
from fastapi import APIRouter, Depends



router = APIRouter(tags=["JWT"])



@router.post("/login", response_model=TokenSchema)
async def issues_jwt_to_user(user: UserSchema = Depends(AuthUtils.validate_user_auth)):
    """
    Возвращает JWT в заголовке, в случае успешной аутентификации через зависимость ( Выдает токен пользователю )
    В тело функции мы попадем только в случае успешной палидации логина и пароля
    :param param:
    :param param:
    :return:
    """
    access_token = JWTUtils.create_access_token(user=user)

    refresh_token = JWTUtils.create_refresh_token(user=user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me", response_model=UserPublicSchema)
async def get_user_profile(
    user: UserPublicSchema = Depends(AuthUtils.get_current_user),
):
    """
    Предоставляет пользователю доступ к своим данным в случае успешной проверки данных в токене через зависимость get_current_user
    :param user:
    :return:
    """
    return user
