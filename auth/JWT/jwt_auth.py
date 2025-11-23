# Для кодирования и декодирования, а так же выпуста JWT токена и его составляющий  используется библиотека pyJWT с расширением Cryptographic
# pip install 'pyJWT[crypto]'

from auth.JWT.schemas.token import TokenSchema
from auth.JWT.schemas.user import UserPublicSchema, UserSchema
from auth.JWT.utils import JWTUtils, AuthUtils, UserDataParser
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
    payload = {"sub": str(user.id), "name": user.name, "emmail": user.email}

    # Генерирует access_token (токен короткого срока действия), для создания токена необходимо передать payload ( полезную нагрузку )
    access_token = JWTUtils.encode_jwt(payload)

    return TokenSchema(access_token=access_token, type_token="Bearer")



@router.get('/me', response_model=UserPublicSchema)
async def get_user_profile(user: UserPublicSchema = Depends(AuthUtils.get_current_user)):
    """
    Предоставляет пользователю доступ к своим данным в случае успешной проверки данных в токене через зависимость get_current_user
    :param user:
    :return:
    """
    return user


