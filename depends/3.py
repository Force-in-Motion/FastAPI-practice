from fastapi import FastAPI, Depends
from starlette.requests import Request

# Зависимости в FastAPI возможно указать как глобальные зависимости. Глобальные зависимости FastAPI могут быть добавлены так же, как мы это сделали с декораторами операций пути.
# Но вместо декораторов мы можем добавить их в само приложение FastAPI.
# Например, мы можем добавить такие транзакции, как регистрация исключений, кэширование, логирование и авторизация пользователей, которые будут общие для любого приложения.
# По аналогии с зависимостями пути, мы можем добавить глобальные зависимости. Изменим в файле main.py создание экземпляра класса FastAPI и добавим новую конечную точку и функцию зависимости:


log_user = []


def log_client(request: Request):
    log_user.append(request.headers)


app = FastAPI(dependencies=[Depends(log_client)])

# Мы написали функционал, в котором все данные посетителей нашего API будут добавляться в список.


@app.get("/log_user")
async def print_log_user():
    return {"user": log_user}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("3:app", reload=True)
