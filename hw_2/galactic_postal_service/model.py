from pydantic import BaseModel


class Parcel(BaseModel):
    """
    Формирует сущность посылки
    """
    id: int = 0
    name: str
    sender: str
    recipient: str
    weight: float
    status: str = None


class ParcelWarehouse:
    """
    Содержит базу данных и ее поведение
    """
    __parcel_warehouse = []

    __status_list = ['lost-in-space', 'black-hole-incident', 'delivered', 'in-transit']


    @classmethod
    def get_max_id(cls):
        """
        Возвращает максимальный id списка данных, если список пуст вернет 0
        """
        if cls.__parcel_warehouse:
            return max(parcel.id for parcel in cls.__parcel_warehouse)
        return 0


    @classmethod
    def get_all_parcels(cls, status: str, recipient: str) -> list | bool:
        """
        Возвращает всех пользователей, хранящихся в базе данных согласно заданным параметрам
        param status: str
        param recipient: str
        :return: list | bool
        """
        parcels = []

        if status not in cls.__status_list:
            return False

        for parcel in cls.__parcel_warehouse:
            if status == parcel.status and recipient == parcel.recipient:
                parcels.append(parcel)

        if not parcels: return False

        return parcels


    @classmethod
    def add_parcel(cls, parcel: Parcel) -> None:
        """
        Добавляет в хранилище новую сущность
        param parcel: Parcel
        :return: None
        """
        if not isinstance(parcel, Parcel):
            raise ValueError('Получен не верный тип данных, ожидался Parcel')

        if len(cls.__parcel_warehouse) >= 1:
            parcel.id = cls.get_max_id() + 1

        cls.__parcel_warehouse.append(parcel)


    @classmethod
    def update_status_parcel(cls, id: int, status: str) -> bool:
        """
        Обновляет статус посылки с полученным id
        param id: int
        param status: str
        return: bool
        """
        if not isinstance(id, int):
            raise ValueError('Получен не верный тип данных, ожидался str')

        if not isinstance(status, str):
            raise ValueError('Получен не верный тип данных, ожидался str')

        for parcel in cls.__parcel_warehouse:
            if id == parcel.id:
                parcel.status = status
                return True

        return False


    @classmethod
    def del_parcel(cls, id: int) -> bool:
        """
        Удаляет из базы данных посылку с полученным id
        param id: int
        return: bool
        """
        if not isinstance(id, int):
            raise ValueError('Получен не верный тип данных, ожидался str')

        for parcel in cls.__parcel_warehouse:
            if id == parcel.id:
                cls.__parcel_warehouse.remove(parcel)
                return True

        return False

