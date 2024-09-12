from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ...schemas.user import ConnectionBase, UserRegister
from ..models.user import User, Connection
from ...core.enums import ConnectionStatus
from sqlalchemy.orm.exc import NoResultFound

def create_user(db: Session, user: UserRegister):
    try:
        db_user = User(username=user.username, hashed_password=user.password, first_name=user.first_name, last_name=user.last_name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise e

def get_users(db: Session) -> List[User]:
    return db.query(User).all()

def inactive_users(db: Session) -> List[User]:
    return db.query(User).filter(User.is_active == False).all()

def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def update_user(db: Session, user: UserRegister, user_id: int) -> User:
    find_user = get_user(db, user_id)
    if find_user:
        find_user.first_name = user.first_name
        find_user.last_name = user.last_name
        find_user.hashed_password = user.password
        db.commit()
        db.refresh(find_user)
    return find_user

def change_activity(db: Session, user_id: int, is_active: bool) -> User:
    find_user = get_user(db, user_id)
    if find_user:
        find_user.is_active = is_active
        db.commit()
        db.refresh(find_user)
    return find_user

def create_connection(db: Session, user_id: int, follower_id: int):
    db_connection = Connection(user_id=user_id, follower_id=follower_id, status=ConnectionStatus.REQUESTED)
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

def update_connection(db: Session, user_id: int, follower_id: int, status: ConnectionStatus):
    db_connection = db.query(Connection).filter(
            or_(
                (Connection.user_id == user_id) & (Connection.follower_id == follower_id),
                (Connection.user_id == follower_id) & (Connection.follower_id == user_id)
            )
        ).first()
    if db_connection:
        db_connection.status = status
        db.commit()
        db.refresh(db_connection)
    return db_connection


def get_all_users_connections(db: Session, user_id: int):
    connections = db.query(Connection).filter(
        or_(Connection.follower_id == user_id, Connection.user_id == user_id),
        Connection.status == ConnectionStatus.CONNECTED
    ).all()

    connections_info = []
    for connection in connections:
        if connection.user_id == user_id:
            other_user = db.query(User).filter(User.id == connection.follower_id).first()
        else:
            other_user = db.query(User).filter(User.id == connection.user_id).first()
        
        connections_info.append(ConnectionBase(
            username = other_user.username,
            status= connection.status
        ))

    return connections_info

def get_connection(db: Session, user_id: int, follower_id: int):
    try:
        connection = db.query(Connection).filter(
            or_(
                (Connection.user_id == user_id) & (Connection.follower_id == follower_id),
                (Connection.user_id == follower_id) & (Connection.follower_id == user_id)
            )
        ).one_or_none()
        if connection is not None:
            if connection.user_id == user_id:
                return {
                    "user_id": connection.user_id,
                    "follower_id": connection.follower_id,
                    "status": connection.status,
                }
            elif connection.follower_id == user_id:
                return {
                    "user_id": connection.follower_id,
                    "follower_id": connection.user_id,
                    "status": connection.status,
                }
    except NoResultFound:
        return None