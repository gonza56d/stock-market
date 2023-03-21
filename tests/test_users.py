from http import HTTPStatus

from api.models.auth import Auth
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

        UsersRepository().save(User(
            email=sign_up.email,
            name='John',
            last_name='Rambo'
        ))
        AuthRepository().save(Auth(
            email=sign_up.email,
            password='Different Password too'
        ))

        response = self.client.post('/users/sign_up', json=sign_up.dict())

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': 'Email already taken'}

    def test_sign_up_credentials_ok(self):
        sign_up = UserSignUp(
            email='test@test.com',
            name='John',
            last_name='Rambo',
            password='nothashedpassowrd'
        )
        self.client.post('/users/sign_up', json=sign_up.dict())

        assert AuthRepository().validate(sign_up.email, sign_up.password)

    def test_sign_up_password_too_short(self):
        request_payload = {
            'email': 'test@test.com',
            'name': 'John',
            'last_name': 'Rambo',
            'password': '0short0'
        }
        response = self.client.post('/users/sign_up', json=request_payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_sign_up_invalid_email(self):
        request_payload = {
            'email': 'notanemail',
            'name': 'John',
            'last_name': 'Rambo',
            'password': 'nothashedpassowrd'
        }
        response = self.client.post('/users/sign_up', json=request_payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
