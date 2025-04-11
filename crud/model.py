from pydantic import BaseModel


class Message(BaseModel):
    id: int
    text: str
    # Устанавливает дефолтную схему показа модели в документации (docs)
    # В данном случае у нас id динамический (увеличивается сам при добавлении нового сообщения) поэтому показывать его в документации не нужно
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "text": "Simple message",
    #             }
    #         ]
    #     }
    # }
