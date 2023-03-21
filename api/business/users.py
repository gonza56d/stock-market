from api.models.auth import Auth
from api.models.users import UserSignUp, User
from api.repositories.auth import AuthRepository
from api.repositories.users import UsersRepository


class UsersBusiness:
    """Business logic related to users."""

    def __init__(self):
        self._users_repository = UsersRepository()
        self._auth_repository = AuthRepository()

    def create_user(self, user_sign_up: UserSignUp) -> None:
        self._users_repository.save(
            User(
                email=user_sign_up.email,
                name=user_sign_up.name,
                last_name=user_sign_up.last_name
            )
        )
        self._auth_repository.save(
            Auth(
                email=user_sign_up.email,
                password=user_sign_up.password
            )
        )
