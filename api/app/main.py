import base64
import requests
from typing import Union, Optional
from pydantic import BaseModel, validator
from fastapi import FastAPI 
import sys
import logging
import json

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.warn('API is starting up')

class Application(BaseModel):
    email : str
    message : Optional[str] = "Leber job seeker"

@app.post("/apply")
def check_application(application:Application):
    try:
        srv_status = requests.get('http://server:8001')
        rq_json = '{"email":"'+ application.email +'", "msg":"request from docker"}'
        rq = requests.get('http://46.21.255.61:8000/link', data = rq_json)
        request_code = rq.json()
        get_data = json.loads(request_code)
        code = get_data.get('code', "smth wrong")
        link = get_data.get('link', "smth wrong")
        print(f'Код для гугл формы = "{code}", вставляйте без кавычек')
        answer = '{"message": "Спасибо! Ваш код в консоли сервера. Заполните, пожалуйста, форму по ссылке ' + link + '"}'

    except Exception as e: 
        logger.warn('код будет доступен, когда все контейнеры работают')
        answer = "Что-то не работает"

    return answer

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}
