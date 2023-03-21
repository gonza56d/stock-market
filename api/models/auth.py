from pydantic import BaseModel


class Auth(BaseModel):

    email: str
    password: str


class AuthToken(BaseModel):

    token: str
