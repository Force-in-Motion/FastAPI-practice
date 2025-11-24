from typing import Optional
from pydantic import BaseModel, ConfigDict


class BookOut(BaseModel):
    """ Схема для возвращения клиенту """
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    year: Optional[int] | None = None
    in_stock: bool = True



class BookIn(BaseModel):
    """ Схема для получения данных от клиента """
    model_config = ConfigDict(from_attributes=True)

    title: str
    author: str
    year: Optional[int] | None = None
    in_stock: bool = True