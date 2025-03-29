from fastapi import FastAPI

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






if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)