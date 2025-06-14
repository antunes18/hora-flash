from logging import disable
from api.models.enums import roles
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, user: User) -> User:
        user.role = roles.Roles.user
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_all_users(self, skip: int, limit: int) -> list[User]:
        result = self.session.execute(
            select(User).filter(User.disabled == False).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    def get_user(self, user_id: int) -> User:
        return (
            self.session.query(User)
            .filter((User.id == user_id) and (User.disabled is not True))
            .first()
        )

    def get_user_by_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_phone_number(self, phone_number: str) -> User:
        return self.session.query(User).filter(User.number == phone_number).first()

    def update_user(self, db_user: User, user: User) -> User:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)

        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def disable_user(self, db_user: User) -> User:
        db_user.disabled = True
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def enable_user(self, db_user: User) -> User:
        db_user.disabled = False
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def set_role(self, db_user: User, role: roles.Roles) -> User:
        db_user.role = role.value
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
