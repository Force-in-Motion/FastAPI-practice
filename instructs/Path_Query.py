from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()


#TODO   Способы передачи данных в запросе как параметры пути. После энд поинта в {} указываются
#TODO   параметры, которые принимает функция-обработчик ( /hello/Sergey/Alekseevich )

@app.get("/hello/{first_name}/{last_name}")
async def welcome_user(first_name: str, last_name: str) -> dict:
    """
    В адресе энд поинта указаны параметры пути first_name и last_name,
    их получает функция welcome_user и обрабатывает в своей логике
    """
    return {"user": f'Hello {first_name} {last_name}'}


@app.get("/order/{order_id}")
async def order(order_id: int) -> dict:
    """
    В адресе энд поинта указан параметр пути order_id, FastAPI видит что функция order ожидает его как тип int
     и самостоятельно выполняет приведение параметра к типу int
    """
    return {"id": order_id}

# ========================================================================================================================


#TODO   Способы передачи данных в запросе как qwery параметры. После энд поинта указываются
#       параметры, которые принимает функция-обработчик ( /user?username=Sergey&age=38 )

@app.get("/user")
async def login(username: str, age: int) -> dict:
    """
    В адресе, после энд поинта ставится ? и после него в формате ключ - значение ( username=Sergey )
    указываются параметры, которые ожидает функция - обработчик, параметны разделены амперсандом &
    """
    return {"user": username, "age": age}

# ========================================================================================================================


#TODO   Также мы можем комбинировать, получая параметры пути и параметры запроса.
#       Причем имея в части URL-адреса фиксированные пути. Несмотря на то, что параметры пути предшествуют параметрам запроса
#       в URL-адресе, нет необходимости следовать порядку при их объявлении в определении функции.

@app.get("/employee/{name}/company/{company}")
async def get_employee(name: str, department: str, company: str) -> dict:
    return {"Employee": name, "Company": company, "Department": department}


# ========================================================================================================================

#TODO   Валидация параметров пути и qwery параметров (параметры запроса ):

#TODO   КЛАСС Path РАБОТАЕТ ТОЛЬКО С ПАРАМЕТРАМИ ПУТИ !!!!!!!

#TODO   Path, используемый для определения параметров пути в маршрутах. Он не только определяет,
#       что параметр пути существует, но и накладывает правила валидации, улучшая работу с API.
#       Класс Path также помогает дать параметрам маршрута больше контекста во время документации,
#       автоматически предоставляемой OpenAPI через Swagger и ReDoc, и действует как валидатор.

#TODO   Конструктор Path можно установить следующие параметры для валидации значений:
#       Общие метаданные:
#       title: Описание параметра, отображаемое в документации.
#       description: Более подробное описание параметра.
#       example: Пример значения параметра.
#       include_in_schema: Параметр позволяет исключить операцию пути из сгенерированной схемы OpenAPI docs
#       Специфичные правила валидации:
#       min_length: Минимальная длина строки для параметра.
#       max_length:  Максимальная длина строки для параметра.
#       pattern: Устанавливает регулярное выражение, которому должно соответствовать значение параметра
#       lt: Значение должно быть меньше указанного.
#       le: Значение должно быть меньше или равно указанному.
#       gt: Значение должно быть больше указанного.
#       ge:Значение должно быть больше или равно указанному.


@app.get("/user/{username}/{age}")
async def login(username: str = Path(min_length=3, max_length=15, description='Enter your username', example='Ilya'),
                age: int = Path(ge=0, le=100, description="Enter your age")) -> dict:

    return {"user": username, "age": age}


#TODO   ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР ЗАПРОСА ( age: int ) ДОЛЖЕН ВСЕГДА ИДТИ ПЕРВЫМ
#       ЕСЛИ ОН НЕ ИМЕЕТ ЗНАЧЕНИЯ ПО УМОЛЧАНИЮ ИНАЧЕ ВОЗНИКНЕТ ОШИБКА !

#TODO   Для FastAPI не имеет значения в какой последовательности указаны ожидаемые параметры в функции и в декораторе
#       Он распознает параметры по их названиям, типам и значениям, ему не важен их порядок.


@app.get("/user/{username}")
async def login_1(age: int,
                username: str = Path(min_length=3, max_length=15, description='Enter your username', example='Ilya')) -> dict:

    return {"user": username, "age": age}

#TODO   Для того чтобы была возможность соблюдать одинаковую последовательность параметров пути в декораторе
#       и в параметрах функции нужно использовать класс Annotated

#TODO   Path - ПАРАМЕТР ВСЕГДА ЯВЛЯЕТСЯ ОБЯЗАТЕЛЬНЫМ, ПОСКОЛЬКУ ОН СОСТАВЛЯЕТ ЧАСТЬ ПУТИ.
#       ЕСЛИ ДЛЯ НЕГО УСТАНОВИТЬ ЗНАЧЕНИЕ ПО УМОЛЧАНИЮ, ТО ЭТО ВЫЗОВЕТ ОШИБКУ.

app.get("/user/{username}")
async def login_2(
                  username: Annotated[str, Path(min_length=3, max_length=15, description='Enter your username', example='Ilya')],
                  age: int) -> dict:

    return {"user": username, "age": age}

# ========================================================================================================================

#TODO   Query
#       Для работы с параметрами строки запроса фреймворк предоставляет класс Query из пакета fastapi,
#       который используется для определения параметров запроса. Параметры запроса передаются в URL-адресе после знака вопроса (?), например:  /items?item_id=123.

#TODO   Общие метаданные:
#       title: Описание параметра, отображаемое в документации.
#       description: Более подробное описание параметра.
#       examples: Пример значения параметра.
#       include_in_schema: Параметр позволяет исключить операцию пути из сгенерированной схемы OpenAPI docs

#TODO   Специфичные правила валидации:
#       min_length: Минимальная длина строки для параметра.
#       max_length:  Максимальная длина строки для параметра.
#       pattern: Устанавливает регулярное выражение, которому должно соответствовать значение параметра
#       lt: Значение должно быть меньше указанного.
#       le: Значение должно быть меньше или равно указанному.
#       gt: Значение должно быть больше указанного.
#       ge:Значение должно быть больше или равно указанному.

#TODO   При использовании Query параметров, могут использоваться значения по умолчанию, поскольку частью пути они не являются

#TODO   Если по каким-то причинам мы хотим использовать Query без Annotated, то следует использовать следующий синтаксис:
#       first_name: str | None = Query(default=None, max_length=10))

#TODO   Также с помощью параметра include_in_schema мы можем исключить данный параметр из документации.
#       first_name: str | None = Query(default=None, include_in_schema=False)

@app.get("/user/{username}")
async def login(
                username: Annotated[str, Path(min_length=3, max_length=15, description='Enter your username', example='Sergey')],
                first_name: Annotated[str | None, Query(max_length=10)] = None) -> dict:

    return {"user": username, "Name": first_name}









if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)