from api.business.exceptions import InvalidCredentials
from api.models.auth import Auth, AuthToken
from api.repositories.auth import AccessTokenRepository, AuthRepository
from api.repositories.users import UsersRepository


class AuthBusiness:
    """Business logic for auth purposes."""

    def __init__(self):
        self._access_token_repository = AccessTokenRepository()
        self._auth_repository = AuthRepository()
        self._users_repository = UsersRepository()

    def validate_token(self, token: str) -> str:
        """Validate if provided token is valid and return user email."""
        return self._access_token_repository.validate(token)

    def authenticate(self, credentials: Auth) -> AuthToken:
        is_valid = self._auth_repository.validate(
            credentials.email,
            credentials.password
        )
        if not is_valid:
            raise InvalidCredentials()

        user = self._users_repository.find(False, email=credentials.email)
        token = self._access_token_repository.generate_access_token(user.email)
        return AuthToken(token=token)
