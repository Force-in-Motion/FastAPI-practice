from fastapi import FastAPI, HTTPException
from model import *

app = FastAPI()

@app.get('/cats')
def get_data():
    """
    Обрабатывает запрос get, запрашивает данные с сервера
    """
    return {'Users': UserStorage.get_all_users()}


@app.post('/cats')
def add_data(user: User):
    """
    Обрабатывает запрос post, отправляет данные на сервер
    """
    UserStorage.add_user(user)
    return {'status': 'ok'}


@app.patch('/cats/{name}/like')
def changes_like(name):
    """
    Обрабатывает запрос patch, изменяет данные на сервере
    """
    result = UserStorage.add_user_like(name)
    if  not result:
        raise HTTPException(status_code=404, detail='Пользователь с таким именем не найден')

    return {'status': 'ok'}



@app.patch('/cats/{name}/dislike')
def changes_dislike(name):
    """
    Обрабатывает запрос patch, изменяет данные на сервере
    """
    result = UserStorage.add_user_dislike(name)
    if  not result:
        raise HTTPException(status_code=404, detail='Пользователь с таким именем не найден')

    return {'status': 'ok'}


@app.delete('/cats/{name}')
def del_data(name):
    """
    Обрабатывает запрос delete, удаляет данные с сервера
    """
    result = UserStorage.del_user(name)
    if  not result:
        raise HTTPException(status_code=404, detail='Пользователь с таким именем не найден')

    return {'status': 'ok'}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)