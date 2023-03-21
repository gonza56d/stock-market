from pymongo import MongoClient

from api.env import Env
from api.models.users import User
from api.repositories.exceptions import NotFound


class UsersRepository:
    """Handle users data with mongo implemented repository."""

    def __init__(self):
        client = MongoClient(Env.MONGO_URI)
        db = client['stock-market']
        self._collection = db['users']

    def save(self, user: User) -> None:
        email_taken = self.find(True, email=user.email)
        if email_taken:
            raise
        self._collection.insert_one(user.dict())

    def find(self, many: bool, **filters):
        result = (
            self._collection.find(filters)
            if many else
            self._collection.find_one(filters)
        )
        if many:
            return [User(**data) for data in result]

        if result:
            return User(**result)
        raise NotFound('user', 'filters', filters)

    def delete(self, **filters) -> None:
        self._collection.delete_many(filters)
