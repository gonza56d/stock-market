from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel
from pymongo import MongoClient

from api.env import Env
from api.repositories.exceptions import NotFound


class MongoRepository(ABC):

    db_prefix: str = ''

    def __init__(self) -> None:
        client = MongoClient(Env.MONGO_URI)

        if self.db_prefix:
            self.db_prefix = f'{self.db_prefix}-'

        db = client[f'{self.db_prefix}stock-market']
        self._collection = db[self.collection_name]

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @property
    @abstractmethod
    def entity(self) -> Type[BaseModel]:
        pass

    @abstractmethod
    def save(self, instance: Type[BaseModel]) -> None:
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
