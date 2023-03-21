from unittest import TestCase

from fastapi.testclient import TestClient

from api.main import app


class ApiTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = TestClient(app)
