from pydantic import BaseModel


class User(BaseModel):
    """
    Формирует сущность пользователя
    """
    name: str
    age: int
    city: str
    floor: str
    like: int  = 0
    dislike: int = 0


class UserStorage:
    """
    Содержит базу данных и ее поведение
    """
    __user_storage = []


    @classmethod
    def add_user(cls, user: User) -> None:
        """
        Добавляет в хранилище новую сущность
        :return: str
        """
        if not isinstance(user, User):
            raise ValueError('Получен не верный тип данных')

        cls.__user_storage.append(user)


    @classmethod
    def get_all_users(cls) -> list:
        """
        Возвращает всех пользователей, хранящихся в базе данных
        :return: list
        """
        return cls.__user_storage


    @classmethod
    def add_user_like(cls, name: str) -> bool:
        """
        Добавляет лайк пользователю если такой существует в базе данных
        :param name: str
        :return: None
        """
        if not isinstance(name, str):
            raise ValueError('Получен не верный тип данных, ожидался str')

        for user in cls.__user_storage:
            if name == user.name:
                user.like += 1
                return True

        return False

    @classmethod
    def add_user_dislike(cls, name: str) -> bool:
        """
        Добавляет дизлайк пользователю если такой существует в базе данных
        :param name: str
        :return: None
        """
        if not isinstance(name, str):
            raise ValueError('Получен не верный тип данных, ожидался str')

        for user in cls.__user_storage:
            if name == user.name:
                user.dislike += 1
                return True

        return False


    @classmethod
    def del_user(cls, name):
        """
        Удаляет пользователя из базы данных
        :param name: str
        :return: None
        """
        if not isinstance(name, str):
            raise ValueError('Получен не верный тип данных, ожидался str')

        for user in cls.__user_storage:
            if name == user.name:
                cls.__user_storage.remove(user)
                return True

        return False