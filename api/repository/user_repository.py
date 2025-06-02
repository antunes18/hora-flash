from sqlalchemy.orm import Session
from api.models.dto.user_dto import UserResponseDTO
from api.models.user import User


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def find_all(db: Session) -> list:
    return db.query(User).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
