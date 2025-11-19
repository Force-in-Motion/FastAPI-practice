from datetime import datetime, timedelta, timezone
import bcrypt
from auth.JWT.schemas.user import UserSchema
import jwt
from auth.JWT.settings import JWTSettings



class JWTUtils:
    """Содержит служебные утилиты для работы с jwt токеном"""

    @staticmethod
    def expire_jwt(payload: dict) -> dict:
        """
        Определяет время действия токена
        :param payload: Полезная нагрузка, данные, которые должны быть
        :return: Обновленный payload, с добавленным временем действия токена
        """
        payload = payload.copy()

    @staticmethod
    def encode_jwt(payload: dict) -> str:
        """
        Собирает токен из полученных данных и кодирует его в base64
        :param payload: Полезная нагрузка, данные, которые должны быть переданы в токене
        :return: Готовый закодированный токен
        """
        private_key: str = (
            JWTSettings.private_key.read_text()
        )  # Метод read_text библиотеки pathlib позволяет автоматически прочитать содержимое файла private.pem

        algorithm: str = (
            JWTSettings.algorithm
        )  # Алгоритм шифрования токена, в данном случае ассиметричный ( участвуют приватный и публичный ключи )

        # Для того чтобы выдать токен, который будет иметь срок действия в минутах,
        # начиная с времени выдачинам нужно получить текущее время и прибавить к нему время действия токена, указанное в настройках

        now = datetime.now(timezone.utc)  # Получвем текущее время

        expire_minutes: int = (
            JWTSettings.access_token_expire
        )  # Получаем Срок действия access токена в минутах из настроек

        expire = now + timedelta(
            minutes=expire_minutes
        )  # Прибавляем к текущему времени now время действия токена, указанное в настройках

        # Формируем измененный payload с добавленным сроком действия access токена
        payload_copy = (
            payload.copy()
        )  # Копируем, полукченный от клиента, payload чтобы не изменять оригинальный

        # В скопированный payload добавляем новый ключ exp со значнием expire ( срок действия access токена, начиная с времени выполнения этого метода )
        # и ключ iat, в котором указано когда токен был выпущен
        payload_copy.update(exp=expire, iat=now)

        encode = jwt.encode(  # Собираем токен во едино
            payload=payload_copy,
            key=private_key,
            algorithm=algorithm,
        )

        return encode

    @staticmethod
    def decode_jwt(token: str) -> str:
        """
        Декодирует полученный токен
        :param token: Закодированный в base64 токен
        :return: Раскодированные данные, переданные в токене ( Head.Payload.Signature)
        """
        public_key: str = (
            JWTSettings.public_key.read_text(),
        )  # Метод read_text библиотеки pathlib позволяет автоматически прочитать содержимое файла public.pem

        algoritm: str = (
            JWTSettings.algoritm,
        )  # Алгоритм шифрования токена, в данном случае ассиметричный ( участвуют приватный и публичный ключи )

        decode = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[
                algoritm
            ],  # Алгоритм передается в виде списка, поскольку параметр ожидается типа Sequence
        )

        return decode

    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Хэширует полученный, в формате строки, пароль в байты
        :param password: Пароль в формате строки
        :return: Пароль в формате байтов
        """
        salt = (
            bcrypt.gensalt()
        )  # генерирует соль — случайную последовательность байтов, которая добавляется к паролю перед хэшированием.
        password_bytes: bytes = password.encode()  # Переводим пароль из строки в байты
        return bcrypt.hashpw(
            password_bytes, salt
        )  # При помощи метода hashpw создаем хэшированный пароль из 2 компонентов password_bytes и salt

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
        return bcrypt.checkpw(
            password=password.encode(),  # Переводим пароль в байты
            hashed_password=hashed_password,
        )

    # @staticmethod
    # def validate_user_auth(
    #     login: str = Form(),
    #     password: str = Form(),
    # ) -> UserSchema:
    #     """
    #     Выполняет валидацию пользователя, если все проверки пройдены то возвращает его
    #     :param login: Логин пользователя введенный в форме
    #     :param password: пароль пользователя введенный в форме
    #     :return: Пользователя
    #     """
    #     unauthorized = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid login or password",
    #     )

    #     inactive = HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="User inactive",
    #     )

    #     user = users_db.get(login) # Ищет пользователя по логину в базе, возвращает если находит его

    #     if not user: # Если пользователя нет - выбрасывает исключение
    #         raise unauthorized

    #     if not JWTUtils.validate_password( # Если пользователь найден, то сравнивает пароли: через метод validate_password хэширует полученный пароль и сравнивает с захэшированным паролем в базе
    #         password=password,
    #         hashed_password=user.password,
    #     ):
    #         raise unauthorized # Если захэшированные пароли не совпадают - выбрасывает исключение

    #     if user.active == False: # Проверяет статус пользователя, если False - выбрасывает исключение

    #         raise inactive

    #     return user # Возвращает данные пользователя если проверки пройдены
    




