from typing import Optional

from pymongo import MongoClient
from redis import Redis

from api.env import Env
from api.models.auth import Auth
from api.repositories.exceptions import NotFound


class AccessTokenRepository:
    """Store and validate users' access token with redis implemented repository."""

    def __init__(self):
        """Initialize connection."""
        self._expiration = int(Env.ACCESS_TOKEN_EXPIRES_IN_SECONDS)
        self._connection = Redis(Env.REDIS_URI)
        ping = self._connection.ping()
        if not ping:
            raise ConnectionError(
                f'Could not connect to redis server at {Env.REDIS_URI}'
            )

    def get_user_id(self, token: str) -> Optional[str]:
        """Get a user_id from provided access token."""
        if not (user_id := self._connection.get(token)):
            raise NotFound('user_id', 'token', token)
        return user_id

    def set_user_id(self, token: str, user_id: str) -> None:
        """Set a user_id with access token as key."""
        self._connection.setex(token, self._expiration, user_id)


class AuthRepository:
    """Store and validate auth credentials."""

    def __init__(self):
        client = MongoClient(Env.MONGO_URI)
        db = client['stock-market']
        self._collection = db['auth']

    def save(self, auth: Auth) -> None:
        email_taken = self.is_taken(email=auth.email)
        if email_taken:
            raise
        self._collection.insert(auth.dict())

    def is_taken(self, email: str):
        taken = self._collection.count({'email': email})
        return taken > 0

    def delete(self, **filters) -> None:
        self._collection.delete_many(filters)
