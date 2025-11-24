from cw_1.exeption import DBExeption
from cw_1.schemas import BookIn, BookOut


class Crud:

    storage: list[BookOut] = []
    count: int = 1


    @classmethod
    async def get_all_records(cls, in_stock: bool = True) -> list[BookOut]:
        """
        Возвращает список книг, хранящихся в БД в зависимости от условия
        :return: список книг, хранящихся в БД
        """
        if in_stock:
            return cls.storage

        return [book for book in cls.storage if book.in_stock == False]


    @classmethod
    async def get_record_by_id(cls, id: int) -> BookOut:
        """
        Возвращает Конкретную книгу, найденную по id
        :param id: Идентификатор объекта в БД
        :return: Объект BookOut
        """
        book = next((book for book in cls.storage if book.id == id), None)

        if not book:
            raise DBExeption.not_found

        return book


    @classmethod
    async def add_record(cls, book_in: BookIn) -> BookOut:
        """
        Создает новую запись в БД
        :param book: Объект BookIn, полученный от пользователя
        :return: Объект BookOut, созданный в БД
        """
        book_out: BookOut = BookOut(id=cls.count, **book_in.model_dump())

        cls.storage.append(book_out)

        cls.count += 1

        return book_out


    @classmethod
    async def update_record(
        cls,
        book_in: BookIn,
        book_out: BookOut,
    ) -> BookOut:
        """
        Обновляет Объект книги в БД
        :param book_in: Объект BookIn, полученный от пользователя
        :param book_out: Объект BookOut, предварительно найденный по id
        :return: Объект BookOut, обновленный в БД
        """
        for key, value in book_in.model_dump().items():
            if value is not None:
                setattr(book_out, key, value)

        return book_out


    @classmethod
    async def del_record_by_id(cls, book_out: BookOut) -> dict:
        """
        Удаляет Объект книги из БД
        :param book: Объект BookOut, предварительно найденный по id
        :return: Объект BookOut, удаленный из БД
        """
        cls.storage.remove(book_out)

        return book_out


    @classmethod
    async def clear_db(cls) -> list[BookOut]:
        """
        Полностью очищает БД
        :return: Пустой список
        """
        cls.storage.clear()
        cls.count = 1
        return cls.storage
