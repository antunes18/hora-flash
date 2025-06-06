from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from api.models.enums.roles import Roles


class UserCreateDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=10, max_length=250)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
    role: Roles = Query(default=Roles.user)


class UserResponseDTO(BaseModel):
    username: str
    email: str
    role: str
    token: str = None


class UserLoginDTO(BaseModel):
    email: str
    password: str
