from fastapi import FastAPI, HTTPException
from service import Service as sv


app = FastAPI()

@app.get('/password')
def return_password(length: str):
    """
    Возвращает случайный пароль заданной длины
    :param length: длинна пароля
    :return: int
    """
    return sv.generates_a_password(length)




@app.get('/gravity')
def return_force_of_attraction(name_planet: str, height: str):
    """
    Возвращает силу притяжения там согласно закону всемирного тяготения
    :param name_planet: название планеты
    :param height: высота над ее поверхностью
    :return: str, float
    """
    result = sv.calculates_force_of_attraction(name_planet, height)

    if not result:
        raise HTTPException(status_code=404, detail="Планета не найдена")

    return result


@app.get('/speeding-fine')
def return_speeding_fine(speed, limit):
    """
    Возвращает размер штрафа исходя из принятых параметров
    :param speed: текущая скорость
    :param limit: разрешенная скорость
    :return: str, int
    """
    return sv.calculates_speeding_fine(speed, limit)


@app.get('/convert/{from_currency}/{to_currency}')
def return_converted_sum_currency(from_currency, to_currency, amount, commission_rate):
    """
    По заданным валютам и их параметрам сервис считает итоговую сумму курса валют
    :param from_currency: валюта
    :param to_currency: валюта
    :param amount: количество float
    :param commission_rate: размер комиссии float
    :return: str, float
    """
    return sv.calculates_exchange_rates(from_currency, to_currency, amount, commission_rate)








if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)

