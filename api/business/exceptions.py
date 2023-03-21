

class InvalidCredentials(Exception):
    """Raised when provided auth credentials aren't valid."""


class EmailTaken(Exception):
    """Raised when the requested email for sign up was already taken."""
