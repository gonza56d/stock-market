from pydantic import BaseModel


class User(BaseModel):

    name: str
    last_name: str
    email: str


class UserSignUp(User):

    password: str
