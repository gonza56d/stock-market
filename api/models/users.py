from pydantic import BaseModel
from pydantic.types import constr


class User(BaseModel):

    name: str
    last_name: str
    email: str


class UserSignUp(User):

    password: constr(min_length=8)
