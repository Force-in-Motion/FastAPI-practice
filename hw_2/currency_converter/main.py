from fastapi import FastAPI, HTTPException, Body
from model import Currency, Currencies
    
app = FastAPI()


@app.get('/exchange-rates')
def exchange_rates():
    """
    Обрабатывает запрос get, запрашивает данные с сервера
    """
    return {'status': 'ok', 'currencies': Currencies.get_all()}


@app.post('/add-currency')
def add_currency(currency: Currency):
    """
    Обрабатывает запрос post, отправляет данные на сервер
    """
    Currencies.add(currency)
    return {'status': 'ok'}


@app.patch('/update-rate/{name}')
def update_rate(name: str, rate: float = Body(embed=True)):
    """
    Обрабатывает запрос patch, изменяет данные на сервере
    """
    result = Currencies.update(name, rate)
    if not result:
        raise HTTPException(status_code=404, detail='Валюта не найдена')

    return {'status': 'ok'}


@app.delete('/rate/{name}')
def del_rate(name: str):
    """
    Обрабатывает запрос delete, удаляет данные с сервера
    """
    result = Currencies.delete(name)
    if not result:
        raise HTTPException(status_code=404, detail='Валюта не найдена')

    return {'status': 'ok'}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)