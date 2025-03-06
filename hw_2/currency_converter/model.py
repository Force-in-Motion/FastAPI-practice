from pydantic import BaseModel

class Currency(BaseModel):
    """
    Формирует сущность курса валют
    """
    name: str
    rate: float


class Currencies:

    __currencies_lst = []

    @classmethod
    def get_all(cls) -> list:
        """
        Возвращает всех пользователей, хранящихся в базе данных
        :return: list
        """
        return cls.__currencies_lst


    @classmethod
    def add(cls, currency: Currency) -> None:
        """
        Добавляет в хранилище новую сущность currency
        :return: None
        """
        if not isinstance(currency, Currency):
            raise ValueError('Получен не верный тип данных, ожидался Currency')

        cls.__currencies_lst.append(currency)


    @classmethod
    def update(cls, name: str, rate: float) -> bool:
        """
        Изменяет данные в таблице согласно условию
        :param name: str
        :param rate: float
        :return: None
        """
        if not isinstance(name, str):
            raise ValueError('Получен не верный тип данных, ожидался str')

        if not isinstance(rate, float):
            raise ValueError('Получен не верный тип данных, ожидался UpdateRate')

        for currency in cls.__currencies_lst:
            if name == currency.name:
                currency.rate = rate
                return True

        return False


    @classmethod
    def delete(cls, name: str) -> bool:
        """
        Удаляет данные из таблицы согласно условию
        :param name: str
        :return: None
        """
        if not isinstance(name, str):
            raise ValueError('Получен не верный тип данных, ожидался str')

        for currency in cls.__currencies_lst:
            if name == currency.name:
                cls.__currencies_lst.remove(currency)
                return True

        return False

