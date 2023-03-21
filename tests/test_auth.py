from http import HTTPStatus

from parameterized import parameterized

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

    def test_authenticate_ok(self):
        response = self.client.post(
            '/auth',
            json={
                'email': self.sign_up.email,
                'password': self.sign_up.password
            }
        )

        assert response.status_code == HTTPStatus.CREATED
        assert 'token' in response.json()

    @parameterized.expand([
        ('test@test.com', 'wrongpassword'),
        ('wrong@email.com', 'nothashedpassowrd'),
        ('wrong@email.com', 'wrongpasswordtoo')
    ])
    def test_authenticate_wrong_credentials(self, email: str, password: str):
        response = self.client.post(
            '/auth',
            json={
                'email': email,
                'password': password
            }
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_auth_wrong_token(self):
        response = self.client.get(
            '/stock-market',
            headers={'Authorization': f'Bearer SomeRandom.WronG.TOKEN!'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
