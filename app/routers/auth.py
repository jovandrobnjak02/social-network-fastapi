from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependency import get_db
from ..services.auth_service import login_user, register_user
from ..schemas.user import UserRegister, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        401: {"description": "Incorrect username or password"}
    }
)

@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db=db, data=data)

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db=db, data=data)
