from unittest import TestCase

from fastapi.testclient import TestClient

from api.env import Env
from api.main import app
from api.repositories.auth import AuthRepository
from api.repositories.base import MongoRepository
from api.repositories.users import UsersRepository


class ApiTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        MongoRepository.db_prefix = 'test'
        self.client = TestClient(app)
        UsersRepository().delete()
        AuthRepository().delete()
        Env.THROTTLING_SECONDS = 0  # disable for faster tests

    def tearDown(self) -> None:
        super().tearDown()
        UsersRepository().delete()
        AuthRepository().delete()
