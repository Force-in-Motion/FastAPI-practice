from fastapi import FastAPI, status, Body

app = FastAPI()


messages_db = {0: "First post in FastAPI"}


@app.get("/")
async def get_all_messages() -> dict:
    """
    Возвращает все сообщения, сохраненные в базе данных
    """
    return {"status": "ok", "messages": messages_db}


@app.get("/message/{message_id}")
async def get_message(message_id: int) -> dict[str, str]:
    """
    Возвращает сообщение с полученным id если такое есть в базе данных
    """
    return {"status": "ok", "message": messages_db.get(message_id)}


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: str = Body()) -> dict[str, str]:
    """
    Добавляет новое сообщение в БД, если словарь пуст то добавляет первое сообщение с ключом (id) 0
    В противном случае находит максимальный ключ (id) и создает новый ключ, увеличив его на 1 и присваивает ему полученное значение
    """
    if not messages_db:
        messages_db[0] = message

    index = int(max(messages_db, key=int)) + 1

    messages_db[index] = message

    return {"message": "Message created!"}


@app.put("/message/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    """
    Получает новое сообщение в теле запроса и id сообщения как qwery параметр,
    которое хранится в базе, присваивает полученному id (ключ в словаре) новое полученное сообщение.
    """
    messages_db[message_id] = message
    return "Message updated!"


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    """
    Удаляет сообщение из базы данных, которое соответствует полученному id
    """
    messages_db.pop(message_id)
    return f"Message ID={message_id} deleted!"


@app.delete("/")
async def kill_message_all() -> dict[str, str]:
    """
    Полностью очищает базу данных
    """
    messages_db.clear()
    return {"status": "ok"}
