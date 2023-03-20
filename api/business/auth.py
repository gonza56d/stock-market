from api.models.users import User


class AuthBusiness:
    """Business logic for auth purposes."""

    def get_user(self, token: str) -> User:
        """Get a user from a valid token."""
        pass
