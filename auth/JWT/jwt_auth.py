# Для кодирования и декодирования, а так же выпуста JWT токена и его составляющий  используется библиотека pyJWT с расширением Cryptographic
# pip install 'pyJWT[crypto]'

from auth.JWT.schemas.token import TokenSchema
from auth.JWT.schemas.user import UserSchema
from auth.JWT.utils import JWTUtils, AuthUtils
from fastapi import APIRouter, Depends, Form, HTTPException, status

router = APIRouter(tags=["JWT"])




# Создаем 2 юзеров для примера
bob = UserSchema(
    id=1,
    name='Bob',
    password=AuthUtils.hash_password('qwerty'),
    email='asd@gmail.com'
)

sam = UserSchema(
    id=2,
    name='Sam',
    password=AuthUtils.hash_password('asdfg')
)

# Создаем базу данных, с диначиским ключем, равным именю пользователя из схемы и схемой в качестве значения
users_db: dict[str, UserSchema] = {
    bob.name: bob,
    sam.name : sam,
}



def validate_user_auth(
        login: str = Form(),
        password: str = Form(),
    ) -> UserSchema:
        """
        Выполняет валидацию пользователя, если все проверки пройдены то возвращает его
        :param login: Логин пользователя введенный в форме
        :param password: пароль пользователя введенный в форме
        :return: Пользователя
        """
        unauthorized = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

        inactive = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive",
        )

        user = users_db.get(login) # Ищет пользователя по логину в базе, возвращает если находит его

        if not user: # Если пользователя нет - выбрасывает исключение
            raise unauthorized

        if not AuthUtils.validate_password( # Если пользователь найден, то сравнивает пароли: через метод validate_password хэширует полученный пароль и сравнивает с захэшированным паролем в базе
            password=password,
            hashed_password=user.password,
        ):
            raise unauthorized # Если захэшированные пароли не совпадают - выбрасывает исключение

        if user.active == False: # Проверяет статус пользователя, если False - выбрасывает исключение

            raise inactive

        return user



@router.post("/login", response_model=TokenSchema)
def issues_jwt_to_user(user: UserSchema = Depends(validate_user_auth)):
    """
    Возвращает JWT в заголовке, в случае успешной аутентификации через зависимость ( Выдает токен пользователю )
    В тело функции мы попадем только в случае успешной палидации логина и пароля
    :param param:
    :param param:
    :return:
    """
    payload = {"sub": user.id, "name": user.name, "emmail": user.email}

    # Генерирует access_token (токен короткого срока действия), для создания токена необходимо передать payload ( полезную нагрузку )
    access_token = JWTUtils.encode_jwt(payload)

    return TokenSchema(access_token=access_token, type_token="Bearer")


