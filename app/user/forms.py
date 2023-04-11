from pydantic import BaseModel


class UserNamePassForm(BaseModel):
    name: str
    password: str


class UserCreateForm(UserNamePassForm):
    pass


class UserResponseForm(BaseModel):
    id: int
    name: str
