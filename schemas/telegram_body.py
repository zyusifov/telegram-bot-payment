from pydantic import BaseModel


class TelegramBody(BaseModel):
    message: dict
