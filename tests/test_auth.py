from http import HTTPStatus

from api.models.users import UserSignUp
from tests import ApiTest


class TestAuth(ApiTest):

    def setUp(self) -> None:
        super().setUp()
        self.sign_up = UserSignUp(
            email='test@test.com',
            name='John',
            last_name='Rambo',
            password='nothashedpassowrd'
        )
        self.client.post('/users/sign_up', json=self.sign_up.dict())

    def test_authenticate(self):
        response = self.client.post(
            '/auth',
            json={
                'email': self.sign_up.email,
                'password': self.sign_up.password
            }
        )

        assert response.status_code == HTTPStatus.CREATED
        assert 'token' in response.json()
