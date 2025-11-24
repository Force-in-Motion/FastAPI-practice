from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status
from cw_1.crud import Crud
from cw_1.schemas import BookIn, BookOut

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookOut], status_code=status.HTTP_200_OK)
async def get_all_books(in_stock: bool = True) -> list[BookOut]:
    """
    Обрабатывает запрос на получение списка книг согласно условия
    :param in_stock: Позволяет определить условие выдачи результата ( все книги / те, которых нет в наличии )
    :return: Список книг согласно условию
    """
    return await Crud.get_all_records(in_stock)


@router.get("/{id}", response_model=BookOut, status_code=status.HTTP_200_OK)
async def get_book_by_id(
    book_out: Annotated[BookOut, Depends(Crud.get_record_by_id)],
) -> BookOut:
    """
    Обрабатывает запрос на получение конкретной книги по ее id
    :param book_out: Схема книги для возврата клиенту, полученная Через зависимость 
    :return: Конкретную книгу
    """
    return book_out


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_out: Annotated[BookOut, Depends(Crud.add_record)],
) -> BookOut:
    """
    Обрабатывает запрос на добавление книги в БД
    :param book_out: Схема книги для возврата клиенту, полученная Через зависимость после добавления в БД
    :return: добавленную в БД книгу
    """
    return book_out


@router.put("/{id}", response_model=BookOut, status_code=status.HTTP_200_OK)
async def update_book_by_id(
    book_in: BookIn,
    book_out: Annotated[BookOut, Depends(Crud.get_record_by_id)],
) -> BookOut:
    """
    Обрабатывает запрос на обновление конкретной книги в БД
    :param book_in: Схема книги, полученная от клиента
    :param book_out: Схема книги для возврата клиенту, полученная Через зависимость после обновления в БД
    :return: Обновленную в БД книгу
    """
    return await Crud.update_record(book_in=book_in, book_out=book_out)


@router.delete("/", response_model=list[BookOut])
async def clear_books(
    list_books_out: Annotated[list, Depends(Crud.clear_db)],
) -> list[BookOut]:
    """
    Полностью очищает БД
    :return: Список
    """
    return list_books_out


@router.delete("/{id}", response_model=BookOut)
async def delete_book_by_id(
    book_out: Annotated[BookOut, Depends(Crud.get_record_by_id)],
) -> BookOut:
    """
    Обрабатывает запрос на удаление конкретной книги из БД
    :param book_out: Схема книги для возврата клиенту, полученная Через зависимость после удаления из БД
    :return: Удаленную из БД книгу
    """
    return await Crud.del_record_by_id(book_out=book_out)
