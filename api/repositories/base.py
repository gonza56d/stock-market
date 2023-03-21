from abc import ABC, abstractmethod
from typing import Any

from pymongo import MongoClient

from api.env import Env
from api.repositories.exceptions import NotFound


class MongoRepository(ABC):

    def __init__(self, db_prefix: str = '') -> None:
        client = MongoClient(Env.MONGO_URI)

        if db_prefix:
            db_prefix = f'{db_prefix}-'

        db = client[f'{db_prefix}stock-market']
        self._collection = db[self.collection_name]

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @property
    @abstractmethod
    def entity(self) -> Any:
        pass

    @abstractmethod
    def save(self, instance) -> None:
        pass

    def find(self, many: bool, **filters):
        result = (
            self._collection.find(filters)
            if many else
            self._collection.find_one(filters)
        )
        if many:
            return [self.entity(**data) for data in result]

        if result:
            return self.entity(**result)
        raise NotFound(self.entity.__name__, 'filters', filters)

    def delete(self, **filters) -> None:
        self._collection.delete_many(filters)
