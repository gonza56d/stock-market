from random import choices
import string
from typing import Any

from redis import from_url as Redis

from api.business.exceptions import EmailTaken
from api.env import Env
from api.models.auth import Auth
from api.repositories.base import MongoRepository
from api.repositories.exceptions import NotFound


class AccessTokenRepository:
    """Store and validate users' access token with redis implemented repository."""

    def __init__(self):
        """Initialize connection."""
        self._expiration = int(Env.ACCESS_TOKEN_EXPIRES_IN_SECONDS)
        self._connection = Redis(Env.REDIS_URI)
        self._connection.ping()

    def validate(self, token: str) -> str:
        """Validate access token and return user email."""
        email = self._connection.get(token)
        if not email:
            raise NotFound('token', 'token', token)
        return email

    def generate_access_token(self, email: str) -> str:
        """Store a user email with access token as key."""
        token = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
        self._connection.setex(token, self._expiration, email)
        return token


class AuthRepository(MongoRepository):
    """Store and validate auth credentials."""

    @property
    def collection_name(self) -> str:
        return 'auth'

    @property
    def entity(self) -> Any:
        return Auth

    def save(self, auth: Auth) -> None:
        email_taken = self.is_taken(email=auth.email)
        if email_taken:
            raise EmailTaken()
        self._collection.insert_one(auth.dict())

    def is_taken(self, email: str):
        taken = self._collection.count_documents({'email': email})
        return taken > 0

    def validate(self, email: str, password: str) -> bool:
        result = self._collection.count_documents(
            {'email': email, 'password': password}
        )
        return result > 0
