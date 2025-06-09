from unittest.mock import AsyncMock
from fastapi import Depends
from sqlalchemy import values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.exceptions.user_exceptions import UserNotFound
from api.models.dto.user_dto import UserResponseDTO
from api.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user: User) -> User:
        await self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all_users(self, skip: int, limit: int) -> list[User]:
        return (
            await self.session.query(User)
            .filter(User.disabled == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_user(self, user_id: int) -> User:
        return (
            await self.session.query(User)
            .filter(User.id == user_id and User.disabled == False)
            .first()
        )

    async def get_user_by_email(self, email: str) -> User:
        return await self.session.query(User).filter(User.email == email).first()

    async def update_user(self, db_user: User, user: User) -> User:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)

        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def disable_user(self, db_user: User) -> User:
        db_user.disabled = True
        await self.session.commit()
        await self.session.refresh(db_user)
        return await db_user

    async def enable_user(self, db_user: User) -> User:
        db_user.disabled = False
        await self.session.commit()
        await self.session.refresh(db_user)
        return await db_user
