from http import HTTPStatus

from api.models.users import User, UserSignUp
from api.repositories.auth import AuthRepository
from api.repositories.users import UsersRepository
from tests import ApiTest


class TestUsers(ApiTest):

    def test_sign_up_ok(self):
        expected_result = {
            'status_code': HTTPStatus.CREATED,
            'json': {},
        }

        sign_up = UserSignUp(
            email='test@test.com',
            name='John',
            last_name='Rambo',
            password='nothashedpassowrd'
        )
        expected_result['user'] = User(**sign_up.dict())
        response = self.client.post('/users/sign_up', json=sign_up.dict())

        assert {
            'status_code': response.status_code,
            'json': response.json(),
            'user': UsersRepository().find(False, email=sign_up.email)
        } == expected_result

    def test_sign_up_email_taken_error(self):
        sign_up = UserSignUp(
            email='test@test.com',
            name='John',
            last_name='Rambo',
            password='nothashedpassowrd'
        )
        self.client.post(
            '/users/sign_up',
            json={
                'email': sign_up.email,
                'name': 'Another Name',
                'last_name': 'Another Last Name',
                'password': 'Different Password too'
            }
        )
        second_response = self.client.post('/users/sign_up', json=sign_up.dict())

        assert second_response.status_code == HTTPStatus.BAD_REQUEST
        assert second_response.json() == {'detail': 'Email already taken'}

    def test_sign_up_credentials_ok(self):
        sign_up = UserSignUp(
            email='test@test.com',
            name='John',
            last_name='Rambo',
            password='nothashedpassowrd'
        )
        self.client.post('/users/sign_up', json=sign_up.dict())

        assert AuthRepository().validate(sign_up.email, sign_up.password)
