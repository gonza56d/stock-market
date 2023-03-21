from unittest import TestCase

from fastapi.testclient import TestClient

from api.main import app
from api.repositories.auth import AuthRepository
from api.repositories.users import UsersRepository


class ApiTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = TestClient(app)

    def tearDown(self) -> None:
        super().tearDown()
        UsersRepository().delete()
        AuthRepository().delete()
