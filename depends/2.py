from fastapi import FastAPI, Depends, Query, HTTPException


app = FastAPI()


# Всегда есть возможность реализовать триггеры, валидаторы и обработчики исключений как внедряемые функции.
# Поскольку эти зависимые объекты работают как фильтры для входящего запроса, их внедрение происходит в операторе пути, а не в списке параметров службы
# Маршрутизатор пути может содержать более одного внедряемого объекта, поэтому для его параметра зависимостей всегда требуется значение списка ([ ])
# При использовании зависимостей в параметрах пути, валидатор(pagination_path_func) приостанавливает выполнение API, чтобы получить параметр page(номер страницы),
# и проверяет его содержание. Мы проверяем параметр page, в случае если он меньше 0, то мы вызываем 404 ошибку, в случае если он равен нулю вызываем 400 ошибку.


async def pagination_path_func(page: int):
    if page < 0:
        raise HTTPException(status_code=404, detail="Page does not exist")
    if page == 0:
        raise HTTPException(status_code=400, detail="Invalid page value")


async def pagination_func(limit: int = Query(10, ge=0), page: int = 1):
    return {"limit": limit, "page": page}


@app.get("/messages", dependencies=[Depends(pagination_path_func)])
async def all_message(pagination: dict = Depends(pagination_func)):
    return {"messages": pagination}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("2:app", reload=True)
