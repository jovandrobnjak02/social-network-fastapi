from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..schemas.response import ResponseMessage
from ..db.crud.user import change_activity, create_connection, get_all_users_connections, get_connection, get_user, get_users, inactive_users, update_connection
from ..db.crud.post import get_users_posts
from ..schemas.user import ConnectionBase, UserProfile
from ..db.models.user import User
from ..core.enums import ConnectionStatus, Role

def get_profile(db: Session, current_user: User, user_id: int):
    if current_user.id == user_id:
        connections = get_all_users_connections(db, current_user.id)
        posts = get_users_posts(db, current_user.id)
        return UserProfile(id= current_user.id, username=current_user.username, first_name=current_user.first_name,
                            last_name=current_user.last_name,
                            connections=connections, posts= posts)
    
    connection = get_connection(db, user_id = current_user.id, follower_id= user_id)
    user = get_user(db, user_id)
    
    if not user.is_active and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot get profile of inactive user")
    
    if connection is None or connection["status"] in [ConnectionStatus.NOT_CONNECTED, ConnectionStatus.REQUESTED]:
        
        return UserProfile(
            id= user.id, 
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            status=ConnectionStatus.NOT_CONNECTED if connection is None or connection["status"] == ConnectionStatus.NOT_CONNECTED else ConnectionStatus.REQUESTED
        )
    
    connections = get_all_users_connections(db, user_id)
    posts = get_users_posts(db, user_id)
    return UserProfile(id= user.id, 
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            status= connection["status"], 
            connections= connections, posts=posts)
    
    
def connect_with_user(db: Session, current_user: User, user_id: int):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot connect with user with the same id")
    user = get_user(db, user_id)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot connect with inactive user")
    
    connection = get_connection(db, user_id = current_user.id, follower_id= user_id)
    
    if connection is None:
        inserted = create_connection(db=db, user_id=current_user.id, follower_id=user_id)
        if inserted is not None:
            return ResponseMessage(msg = "Connection successfully requested!")
    
    if connection['status'] == ConnectionStatus.CONNECTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Users already connected!")
    elif connection['status'] == ConnectionStatus.REQUESTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Connection already requested!")
    elif connection['status'] == ConnectionStatus.NOT_CONNECTED:
        update_connection(db, connection["user_id"], connection["follower_id"], ConnectionStatus.REQUESTED )
        return ResponseMessage(msg = "Connection successfully requested!")
    
    
    return ResponseMessage(msg = "Failed to request connection")

def update_users_connection(db: Session, current_user: User, user_id: int, update_type: str):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot change connection type")
    
    connection = get_connection(db, user_id = current_user.id, follower_id= user_id)

    user = get_user(db, connection["follower_id"])
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot connect with inactive user")
    
    if connection is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Connection non existent")
    
    if update_type == "accept" and connection["status"] == ConnectionStatus.REQUESTED:
        connection_status = ConnectionStatus.CONNECTED
    
    elif (update_type == "decline" and connection["status"] == ConnectionStatus.REQUESTED) or  (update_type == "disconnect" and connection["status"] == ConnectionStatus.CONNECTED):
        connection_status = ConnectionStatus.NOT_CONNECTED
    
    updated_connection = update_connection(db, connection["user_id"], connection["follower_id"], connection_status )
    user = get_user(db, updated_connection.follower_id)
    return ConnectionBase(username=user.username, status= updated_connection.status)


def change_users_activity(db: Session, current_user: User, user_id: int, is_active: bool):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non admin users cannot change user activity")
    
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot deactivate yourself!")
    
    return change_activity(db, user_id, is_active)

def get_all_users(db: Session, current_user: User):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non admin users cannot get full user list")
    
    return get_users(db)

def get_inactive_users(db: Session, current_user: User):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non admin users cannot get full user list")
    
    return inactive_users(db)