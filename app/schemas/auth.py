from pydantic import BaseModel
from ..core.enums import Role

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None