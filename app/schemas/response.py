from pydantic import BaseModel


class ResponseMessage(BaseModel):
    msg: str