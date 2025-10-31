в FastAPI (и HTTP вообще) данные действительно могут приходить из четырёх основных источников, и FastAPI умеет чётко разделять, откуда что взялось.

Давай разберём это структурно и на простом примере 👇

🔹 1. Источники данных в запросе
Тип данных	Где находится	Пример в HTTP-запросе	Как принимается в FastAPI
Path parameters	В самом пути (URL)	GET /users/123	@app.get("/users/{user_id}") → user_id: int
Query parameters	После знака ? в URL	GET /users?active=true&page=2	@app.get("/users") → active: bool, page: int
Body (JSON / form-data)	В теле запроса (POST, PUT, PATCH)	{"username": "alice", "password": "s3cr3t"}	@app.post("/login") → user: UserModel
Headers	В заголовках запроса	Authorization: Bearer token123	Header или Request.headers
(опционально) Cookies	В заголовке Cookie:	Cookie: session_id=abc123	Cookie или Request.cookies
🧩 2. Пример — всё сразу в одном запросе
from fastapi import FastAPI, Header, Query, Path, Body
from pydantic import BaseModel

app = FastAPI()

class UserData(BaseModel):
    username: str
    password: str

@app.post("/users/{user_id}")
async def handle_user(
    user_id: int = Path(..., description="ID пользователя из пути"),
    active: bool = Query(True, description="Активен ли пользователь"),
    token: str | None = Header(None, description="Токен авторизации"),
    data: UserData = Body(..., description="Тело запроса (JSON)"),
):
    return {
        "path_param": user_id,
        "query_param": active,
        "header": token,
        "body": data.dict(),
    }

🧠 3. Как это выглядит на практике
Пример запроса (HTTP):
POST /users/42?active=true HTTP/1.1
Host: example.com
Authorization: Bearer abc123
Content-Type: application/json

{
  "username": "alice",
  "password": "wonderland"
}

Что получит FastAPI:
Источник	Пример данных	Как ты их получаешь
Path	42	user_id: int
Query	active=true	active: bool
Header	Authorization: Bearer abc123	token: str
Body	{"username": "alice", "password": "wonderland"}	data: UserData
🧠 4. Почему FastAPI это разделяет

FastAPI не просто всё кладёт “в кучу” — он:

валидирует каждый источник отдельно через Pydantic,

автоматически документирует всё в Swagger UI (/docs),

и при конфликте имён (например, параметр id и в пути, и в query) — точно знает, откуда какой брать.

💡 5. Ещё один полезный факт

Query, Path, Header, Cookie — это “dependency параметризаторы”,
то есть FastAPI через них понимает, из какого места брать значение.

Если ты просто напишешь param: int, то он будет искать его в query по умолчанию.

Если у тебя есть Pydantic модель — она автоматически мапится на JSON тело запроса.

🔍 6. Краткий пример отличий
@app.get("/items/{item_id}")
async def example(
    item_id: int,           # Path
    q: str | None = None,   # Query
    user_agent: str = Header(...),  # Header
):
    return {"id": item_id, "query": q, "agent": user_agent}


Если ты вызовешь:

GET /items/10?q=test
User-Agent: Mozilla/5.0


→ FastAPI вернёт:

{
  "id": 10,
  "query": "test",
  "agent": "Mozilla/5.0"
}


✅ Итоговое понимание:

Да, в FastAPI данные могут приходить из разных “слоёв” HTTP-запроса:
Path, Query, Body, Headers (+ Cookies).

И FastAPI умеет автоматически разбирать и валидировать каждую часть независимо.