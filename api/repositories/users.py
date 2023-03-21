from typing import Any

from api.business.exceptions import EmailTaken
from api.models.users import User
from api.repositories.base import MongoRepository


class UsersRepository(MongoRepository):
    """Handle users data with mongo implemented repository."""

    @property
    def collection_name(self) -> str:
        return 'users'

    def save(self, user: User) -> None:
        email_taken = self.find(True, email=user.email)
        if email_taken:
            raise EmailTaken()
        self._collection.insert_one(user.dict())

    @property
    def entity(self) -> Any:
        return User
