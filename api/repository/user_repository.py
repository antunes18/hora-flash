from sqlalchemy import select
from sqlalchemy.orm.session import Session
from api.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_all_users(self, skip: int, limit: int) -> list[User]:
        result = self.session.execute(
            select(User).filter(User.disabled is False).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    def get_user(self, user_id: int) -> User:
        return (
            self.session.query(User)
            .filter(User.id == user_id and User.disabled == False)
            .first()
        )

    def get_user_by_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

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
