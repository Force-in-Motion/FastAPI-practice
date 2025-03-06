from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class Currency(BaseModel):
    id: int
    code: str # Название валюты
    rate_to_usd: float


class Currencies:

    __currencies_lst = [ Currency(id = 1, code = 'USD', rate_to_usd = 4.8), Currency(id = 2, code = 'EUR', rate_to_usd = 12.9)]

    @classmethod
    def append(cls, currency: Currency):
        cls.__currencies_lst.append(currency)


    @classmethod
    def get_all(cls):
        return cls.__currencies_lst
    
app = FastAPI()
lst = Currencies.get_all()

@app.get('/exchange-rates')
def exchange_rates():
    currencies = map(lambda currency: {'code': currency.code, 'rate_to_usd': currency.rate_to_usd}, Currencies.get_all())
    currencies = list(currencies)
    return {'status': 'ok', 'currencies': currencies}


@app.post('/add-currency')
def add_currency(currency: Currency):

    Currencies.append(currency)

    return {'status': 'ok'}


@app.patch('/update-rate')
def update_rate(currency: Currency):

    for elem in lst:
        if currency.id not in lst:
            raise ValueError('Запись с таким ключом отсутствует')
            
        if elem.id == currency.id:
            elem.rate_to_usd = currency.rate_to_usd

            return {'status': 'ok'}


@app.delete('/rate')
def del_rate(currency: Currency):

    for elem in lst:
        if currency.id not in lst:
            raise ValueError('Запись с таким ключом отсутствует')
        
        if elem.id == currency.id:
            lst.remove(elem)

            return {'status': 'ok'}
            

app.mount('/', StaticFiles(directory='./static', html=True), name='static')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)