from os import environ
from typing import Optional


class EnvError(Exception):

    def __init__(self, envvar: str):
        super().__init__(f'The requested envvar "{envvar}" could not be found.')


class Env:
    """Provide all the environment variables."""

    @staticmethod
    def load(envvar: str, as_: Optional[type] = None):
        """Strictly load the provided envvar value or raise EnvError."""
        if not (result := environ.get(envvar)):
            raise EnvError(envvar)
        return as_(result) if as_ is not None else result

    REDIS_URI = load('REDIS_URI')
    ACCESS_TOKEN_EXPIRES_IN_SECONDS = load('ACCESS_TOKEN_EXPIRES_IN_SECONDS', int)
    MONGO_URI = load('MONGO_URI')
    ALPHAVANTAGE_API_KEY = load('ALPHAVANTAGE_API_KEY')
    THROTTLING_SECONDS = load('THROTTLING_SECONDS', int)
