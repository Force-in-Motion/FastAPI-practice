from datetime import datetime, timedelta, timezone
from turtle import st
import bcrypt
from auth.JWT.schemas.user import UserPublicSchema, UserSchema
from auth.JWT.exeption import DBExeption
import jwt
from auth.JWT.settings import jwt_settings
from fastapi import Form, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer




oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login') # Это объект зависимости FastAPI, который не создаёт токены сам, а лишь извлекает токен из заголовка Authorization: Bearer <token> и возвращает его как строку. Параметр tokenUrl нужен Swagger UI для кнопки Authorize — чтобы знать, куда отправлять форму username/password и получать токен.




class JWTUtils:
    """Содержит служебные утилиты для работы с jwt токеном"""

    @staticmethod
    def expire_jwt(expire_minuts: int) -> dict:
        """
        Возвращает время действия refresh  или access токена
        :param expire_minuts: Определяет время действия токена в минутах в зависимости от от переданных настроек ( access_token_expire: int = 15 или refresh_token_expire: int = 60 * 24 * 30 )
        :return: время действия токена в минутах и текущее время
        """
        # Для того чтобы выдать токен, который будет иметь срок действия в минутах,
        # начиная с времени выдачинам нужно получить текущее время и прибавить к нему время действия токена, указанное в настройках

        now = datetime.now(timezone.utc) # Получвем текущее время

        expire = now + timedelta(minutes=expire_minuts) # Прибавляем к текущему времени now время действия токена, указанное в настройках

        # JWT ожидает числа секунд от Unix Epoch, а не объекты datetime, поэтому применяем метод timestamp к полученным данным,
        # а поскольку timestamp возвращает float тип нам нужно перевести его в int
        return { # Создаем готовый словарь, данные из которого нужно будет добавить в payload
            "exp": int(expire.timestamp()), # срок действия access токена, начиная с времени выполнения этого метода 
            "iat": int(now.timestamp()) # ключ iat, в котором указано когда токен был выпущен
        }


    @staticmethod
    def encode_jwt(payload: dict) -> str:
        """
        Собирает токен из полученных данных и кодирует его в base64
        :param payload: Полезная нагрузка, данные, которые должны быть переданы в токене
        :return: Готовый закодированный токен
        """
        token = jwt.encode( # Собираем токен во едино
            payload=payload, # Скопированный payload с добавленными ключами exp и iat и их значениями
            key=jwt_settings.private_key.read_text(), # Приватный ключ для кодирования
            algorithm=jwt_settings.algorithm, # Алгоритм шифрования токена, в данном случае ассиметричный ( участвуют приватный и публичный ключи )
        )

        return token


    @staticmethod
    def decode_jwt(token: str) -> str:
        """
        Декодирует полученный токен
        :param token: Закодированный в base64 токен
        :return: Раскодированные данные, переданные в токене payload
        """
        payload = jwt.decode( # Достаем payload из токена
            jwt=token, # Токен в виде строки
            key=jwt_settings.public_key.read_text(), # Публичный ключ для декодирования
            algorithms=[jwt_settings.algorithm], # Алгоритм передается в виде списка, поскольку параметр ожидается типа Sequence
        )

        return payload
    

    @staticmethod
    def create_jwt(
        user: UserSchema,
        token_type: str,
        expire_minuts: int
    ) -> str:
        """
        
        :param user:
        :return:
        """
        payload = {'token_type': token_type, "sub": str(user.id), "name": user.name, "emmail": user.email}

        # В payload добавляем новый ключ exp со значнием expire ( срок действия access токена, начиная с времени выполнения этого метода )
        # и ключ iat, в котором указано когда токен был выпущен
        payload.update(JWTUtils.expire_jwt(expire_minuts=expire_minuts)) # Метод update обовит payload_copy денными из словаря, который возвращает метод expire_jwt, то есть добавит в payload_copy новые ключи и их значения

        # Генерирует access_token (токен короткого срока действия), для создания токена необходимо передать payload ( полезную нагрузку )
        return JWTUtils.encode_jwt(payload)


    @staticmethod
    def create_access_token(user: UserSchema) -> str:
        """
        Декодирует полученный токен
        :param token: Закодированный в base64 токен
        :return: Раскодированные данные, переданные в токене payload
        """
        return JWTUtils.create_jwt(
            user=user,
            token_type=jwt_settings.access_name,
            expire_minuts=jwt_settings.access_token_expire)


    @staticmethod
    def create_refresh_token(user: UserSchema) -> str:
        """
        Декодирует полученный токен
        :param token: Закодированный в base64 токен
        :return: Раскодированные данные, переданные в токене payload
        """
        return JWTUtils.create_jwt(
            user=user,
            token_type=jwt_settings.refresh_name,
            expire_minuts=jwt_settings.refresh_token_expire)





class AuthUtils:


    @staticmethod
    def check_user_status(user: UserSchema) -> UserSchema:
        """
        Проверяет статус пользователя, возвращает его же если статус не False, то есть пользователеь не заблокипран иначе выбрасывает исключение
        :param user: Пользователь из БД
        :return: Возвращает пользователя
        """
        if user.active == False: # Проверяет статус пользователя, если False - выбрасывает исключение

            raise DBExeption.inactive

        return user


    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Хэширует полученный, в формате строки, пароль в байты
        :param password: Пароль в формате строки
        :return: Пароль в формате байтов
        """
        salt = bcrypt.gensalt() # генерирует соль — случайную последовательность байтов, которая добавляется к паролю перед хэшированием.

        password_bytes: bytes = password.encode() # Переводим пароль из строки в байты

        return bcrypt.hashpw(password_bytes, salt) # При помощи метода hashpw создаем хэшированный пароль из 2 компонентов password_bytes и salt
    

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        """
        Проверяет соответствие, введенного пользователем, пароля в виде строки сохраненному паролю в байтах
        :param password: Полученный от пользователя пароль
        :param hashed_password: Сохраненный пароль пользователя при регистрации
        :return: True | False
        """
        return bcrypt.checkpw( # Проверяет соответствие, введенного пользователем, пароля в виде строки сохраненному паролю в байтах 
            password=password.encode(), # Переводим полученный от пользователя в байты и передаем в метод
            hashed_password=hashed_password # # Передаем хэшированный пароль пользователя, сохнаненный в базе
        )


    @staticmethod
    def validate_user_auth(form_data: OAuth2PasswordRequestForm = Depends()) -> UserSchema:
        """
        Выполняет валидацию пользователя, если все проверки пройдены то возвращает его
        :param form_data: При помощи Depends() создается объект OAuth2PasswordRequestForm, содержащий данные, введенные в форме клиента form_data.username и form_data.password
        :return: Пользователя
        """
        user = users_db.get(form_data.username) # Ищет пользователя по логину в базе, возвращает если находит его

        if not user: # Если пользователя в БД нет - выбрасывает исключение
            raise DBExeption.unauthorized

        if not AuthUtils.validate_password( # Если пользователь найден, то сравнивает пароли: через метод validate_password хэширует полученный пароль и сравнивает с захэшированным паролем в БД
            password=form_data.password,
            hashed_password=user.password,
        ):
            raise DBExeption.unauthorized # Если захэшированные пароли не совпадают - выбрасывает исключение

        return AuthUtils.check_user_status(user)  # Проверяет статус пользователя, если True - возвращает пользователя, иначе выбросит исключение



    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> UserPublicSchema:
        """
        Через зависимость oauth2_scheme извлекает токен из заголовка запроса, затем парсит данные, извлеченные из токена и выполняет проверки
        :return: Возвращает пользователя, если такой существует в БД
        """
        payload = JWTUtils.decode_jwt(token) # Декодирует токен и достает payload

        user_name = payload.get('name') # Получает имя пользователя из payload
        
        user = users_db.get(user_name) # Проверяет наличие пользователя в БД по его имени

        if not user:
            raise DBExeption.not_found
        
        user = AuthUtils.check_user_status(user=user) # Проверяет статус пользователя, если True - возвращает пользователя, иначе выбросит исключение

        return user


    




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