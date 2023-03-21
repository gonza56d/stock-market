from api.repositories.auth import AccessTokenRepository


class AuthBusiness:
    """Business logic for auth purposes."""

    def __init__(self):
        self._access_token_repository = AccessTokenRepository()

    def get_user_id(self, token: str) -> str:
        """Get a user_id from a valid token."""
        return self._access_token_repository.get_user_id(token)
