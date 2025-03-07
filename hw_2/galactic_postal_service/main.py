from fastapi import FastAPI, HTTPException, Body
from model import Parcel, ParcelWarehouse as pw

app = FastAPI()

@app.get("/parcels")
def get_parcels(status: str, recipient: str) -> dict:
    """
    Обрабатывает запрос get, запрашивает данные с сервера cсогласно заданным параметрам
    """
    result = pw.get_all_parcels(status, recipient)

    if not result:
        raise HTTPException(status_code=404, detail='По заданным параметрам данные отсутствуют')

    return {'status': 'ok', 'parcels': result}


@app.post('/parcels')
def add_parcel(parcel: Parcel) -> dict:
    """
    Обрабатывает запрос post, отправляет данные на сервер
    """
    pw.add_parcel(parcel)

    return {'status': 'ok'}


@app.patch('/parcels/{id}')
def update_status_parcel(id: int, status: str = Body(embed=True)) -> dict:
    """
    Обрабатывает запрос patch, изменяет данные на сервере cсогласно заданным параметрам
    """
    result = pw.update_status_parcel(id, status)

    if not result:
        raise HTTPException(status_code=404, detail='По заданным параметрам данные отсутствуют')

    return {'status': 'ok'}


@app.delete('/parcels/{id}')
def del_parcel(id: int) -> dict:
    """
    Обрабатывает запрос delete, удаляет данные с сервера cсогласно заданным параметрам
    """
    result = pw.del_parcel(id)

    if not result:
        raise HTTPException(status_code=404, detail='По заданным параметрам данные отсутствуют')

    return {'status': 'ok'}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)