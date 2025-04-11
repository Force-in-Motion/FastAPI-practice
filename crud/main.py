from fastapi import FastAPI, Body, HTTPException, Path, Query, Request, Form
from fastapi.templating import (
    Jinja2Templates,
)  # Работает с шаблонами html написанными в папке templates
from fastapi.responses import (
    HTMLResponse,
)  # Нужен, чтобы возвращать шаблоны html кода, написанные в шаблонах
from typing import Annotated
from model import Message

app = FastAPI()
templates = Jinja2Templates(
    directory="crud/templates"
)  # Определяет путь к папке, в которой хранятся шаблоны html. Теперь Jinja понимает, что нужно искать HTML-файлы внутри этой папки шаблонов.

messages_db = []


@app.get("/")
async def get_all_messages(request: Request) -> HTMLResponse:
    """
    Возвращает все сообщения, сохраненные в базе данных
    """
    return templates.TemplateResponse(
        request, "message.html", {"messages": messages_db}
    )


@app.get("/message/{message_id}")
async def get_message(
    request: Request, message_id: Annotated[int, Path()]
) -> HTMLResponse:
    """
    Возвращает сообщение с полученным id если такое есть в базе данных
    """
    if not message_id in messages_db:
        raise HTTPException(status_code=404, detail="Message not found")
    return templates.TemplateResponse(
        request, "message.html", {"message": messages_db[message_id]}
    )


@app.post("/")
async def create_message(
    request: Request, message: Annotated[str, Form()]
) -> HTMLResponse:
    """
    Добавляет новое сообщение в БД, если список пуст то добавляет первое сообщение с полем id = 0
    В противном случае находит максимальное поле id и создает новый ключ, увеличив его на 1
    Затем добавляет сообщение в список.
    """
    if messages_db:
        max_id_message = max(messages_db, key=lambda m: m.id).id + 1
    else:
        max_id_message = 0
    messages_db.append(Message(id=max_id_message, text=message))
    return templates.TemplateResponse(
        request, "message.html", {"messages": messages_db}
    )


@app.put("/message/{message_id}")
async def update_message(
    message_id: Annotated[int, Path()], message: Annotated[str, Body()]
) -> str:
    """
    Получает новое сообщение в теле запроса и id сообщения как qwery параметр,
    которое хранится в базе, присваивает полученному id (ключ в словаре) новое полученное сообщение.
    """
    if not message_id in messages_db:
        raise HTTPException(status_code=404, detail="Message not found")

    messages_db[message_id].text = message

    return "Message updated!"


@app.delete("/message/{message_id}")
async def delete_message(message_id: Annotated[int, Path()]) -> str:
    """
    Удаляет сообщение из базы данных, которое соответствует полученному id
    """
    if not message_id in messages_db:
        raise HTTPException(status_code=404, detail="Message not found")

    messages_db.pop(message_id)

    return f"Message ID={message_id} deleted!"


@app.delete("/")
async def kill_message_all() -> dict[str, str]:
    """
    Полностью очищает базу данных
    """
    messages_db.clear()
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("test:app", reload=True)
