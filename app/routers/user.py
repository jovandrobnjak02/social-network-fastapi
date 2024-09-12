from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ..schemas.response import ResponseMessage
from ..services.user_service import change_users_activity, get_all_users, get_inactive_users, get_profile, connect_with_user, update_users_connection
from ..schemas.user import ConnectionBase, UserActivityChange, UserId, UserProfile
from ..db.models.user import User
from ..dependency import get_db
from ..core.security import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        401: {"description": "Incorrect username or password"},
        400: {"description": "User already connected"}
    }
)

@router.get("/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: Annotated[int, Path(title="The ID of the user whose profile to get")],current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_profile(db=db, current_user=current_user, user_id=user_id)


@router.post("/{user_id}/connect",response_model=ResponseMessage)
async def connect(user_id: Annotated[int, Path(title="The ID of the user to connect to")],current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db), ):
    return connect_with_user(db=db, current_user=current_user, user_id=user_id)

@router.put("/{user_id}/accept", response_model= ConnectionBase)
async def accept_connection(user_id: Annotated[int, Path(title="The ID of the user to accept")],current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return update_users_connection(db=db, current_user=current_user, user_id=user_id, update_type="accept")

@router.put("/{user_id}/decline", response_model= ConnectionBase)
async def decline_connection(user_id: Annotated[int, Path(title="The ID of the user to decline")],current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db) ):
    return update_users_connection(db=db, current_user=current_user, user_id=user_id, update_type="decline")

@router.put("/{user_id}/disconnect", response_model= ConnectionBase)
async def disconnect_connection(user_id: Annotated[int, Path(title="The ID of the user to disconnect from")],current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db) ):
    return update_users_connection(db=db, current_user=current_user, user_id=user_id, update_type="disconnect")

@router.put("/{user_id}/activity", tags=["admin"])
async def change_activity(activity_change: UserActivityChange, user_id: Annotated[int, Path(title="The ID of the user to disconnect from")],current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db) ):
    return change_users_activity(db=db, current_user=current_user, user_id=user_id, is_active= activity_change.is_active)

@router.get("/", tags=["admin"])
async def all_users(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_all_users(db, current_user)

@router.get("/inactive", tags=["admin"])
async def all_inactive_users(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_inactive_users(db, current_user)