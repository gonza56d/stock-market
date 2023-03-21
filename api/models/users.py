from pydantic import BaseModel, EmailStr
from pydantic.types import constr


class User(BaseModel):

    name: str
    last_name: str
    email: EmailStr


class UserSignUp(User):

    password: constr(min_length=8)
