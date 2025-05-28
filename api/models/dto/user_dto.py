from pydantic import BaseModel, EmailStr, Field


class UserCreateDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=10, max_length=250)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)


class UserResponseDTO(BaseModel):
    username: str
    email: str
    access_token: str = ""


class UserLoginDTO(BaseModel):
    email: str
    password: str
