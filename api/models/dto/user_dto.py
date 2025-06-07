from fastapi import Query
from pydantic import BaseModel, Field
from api.models.enums.roles import Roles


class UserCreateDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=10, max_length=250)
    number: str = Field(pattern=r"^\d{13,}$", min_length=13, max_length=13)
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
    username: str
    email: str
    number: int
    role: str
    disabled: bool
    access_token: str = None

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    email: str = Field(min_length=10, max_length=250)
    password: str = Field(min_length=8, max_length=128)

    class Config:
        from_attributes = True
