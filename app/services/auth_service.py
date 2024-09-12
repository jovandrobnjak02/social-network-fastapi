from datetime import timedelta
from fastapi import HTTPException, status

from ..schemas.response import ResponseMessage
from ..core.security import authenticate_user, create_access_token, get_password_hash
from ..schemas.user import UserLogin, UserRegister
from sqlalchemy.orm import Session
from ..core.config import settings
from ..schemas.auth import Token
from ..db.crud.user import create_user

def login_user(db: Session, data: UserLogin):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": {"user_id": user.id }}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

def register_user(db: Session, data: UserRegister):
    data.password = get_password_hash(data.password)
    try:
        create_user(db, data)
        return ResponseMessage(msg = f"{data.first_name} {data.last_name} successfully registered with username {data.username}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))