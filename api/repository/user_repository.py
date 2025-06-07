from fastapi import Depends
from sqlalchemy import values
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.exceptions.user_exceptions import UserNotFound
from api.models.dto.user_dto import UserResponseDTO
from api.models.user import User


def create_user(user: User, db: Session) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(skip: int, limit: int, db: Session) -> list[User]:
    return db.query(User).filter(User.disabled == False).offset(skip).limit(limit).all()


def get_user(user_id: int, db: Session) -> User:
    return db.query(User).filter(User.id == user_id and User.disabled == False).first()


def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(username: str, db: Session) -> User:
    return db.query(User).filter(User.username == username).first()


def update_user(db_user: User, user: User, db: Session) -> User:
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def disable_user(db_user: User, db: Session) -> User:
    db_user.disabled = True
    db.commit()
    db.refresh(db_user)
    return db_user


def enable_user(db_user: User, db: Session) -> User:
    db_user.disabled = False
    db.commit()
    db.refresh(db_user)
    return db_user
