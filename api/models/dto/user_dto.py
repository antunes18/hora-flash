from dataclasses import dataclass
from types import ClassMethodDescriptorType
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from api.models.enums.roles import Roles
from api.models.user import User


class UserCreateDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=10, max_length=250)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
    role: Roles = Query(default=Roles.user)

    class Config:
        from_attributes = True


class UserUpdateDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    class Config:
        from_attributes = True


class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str
    role: str
    disabled: bool
    access_token: str = None

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
