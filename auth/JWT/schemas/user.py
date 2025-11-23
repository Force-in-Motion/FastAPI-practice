from pydantic import BaseModel, ConfigDict, EmailStr

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True) # Параметр strict=True говорит что типы данных должны быть строго такими, какие указаны в анотации к параметрам схемы. В обычном режиме → Pydantic преобразует "25" в 25. from_attributes=True Позволяет создавать модель из обычных объектов (ORM-объектов, классов, сущностей), а не только из словарей.
    id: int
    name: str
    password: bytes # Пароль будет захэширован в байты, поэтому в схеме мы храним сразу байты
    email: EmailStr | None = None
    active: bool = True


class UserPublicSchema(BaseModel):
    # Схема для отправки данных пользователю, передаем только безопасные данные исключая служебные, такие как пароль и статус
    model_config = ConfigDict(strict=True, from_attributes=True) # Параметр strict=True говорит что типы данных должны быть строго такими, какие указаны в анотации к параметрам схемы. В обычном режиме → Pydantic преобразует "25" в 25. from_attributes=True Позволяет создавать модель из обычных объектов (ORM-объектов, классов, сущностей), а не только из словарей.
    id: int
    name: str
    email: EmailStr | None = None