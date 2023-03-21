from os import environ


class EnvError(Exception):

    def __init__(self, envvar: str):
        super().__init__(f'The requested envvar "{envvar}" could not be found.')


class Env:
    """Provide all the environment variables."""

    @staticmethod
    def load(envvar: str):
        """Strictly load the provided envvar value or raise EnvironmentError."""
        if not (result := environ.get(envvar)):
            raise EnvError(envvar)
        return result

    REDIS_URI = load('REDIS_URI')
    ACCESS_TOKEN_EXPIRES_IN_SECONDS = load('ACCESS_TOKEN_EXPIRES_IN_SECONDS')
    MONGO_URI = load('MONGO_URI')
