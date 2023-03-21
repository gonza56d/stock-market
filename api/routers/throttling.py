from functools import wraps
from http import HTTPStatus

from fastapi import HTTPException
from starlette.datastructures import Address

from redis import from_url as Redis

from api.env import Env
from api.exceptions import InvalidDependency


redis_client = Redis(Env.REDIS_URI)


def address_in_memory(address: Address) -> bool:
    result = redis_client.get(address.host)
    return result is not None


def check_throttling(client: Address) -> None:
    found = address_in_memory(client)
    if found:
        raise HTTPException(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            detail='Too many requests'
        )


def set_throttling(client: Address) -> None:
    if Env.THROTTLING_SECONDS != 0:
        redis_client.setex(client.host, int(Env.THROTTLING_SECONDS), client.host)


def validate_throttling(function):

    @wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            client = kwargs['request'].client
        except (KeyError, AttributeError):
            raise InvalidDependency('Decorated view must depend a Request object.')
        else:
            check_throttling(client)
            set_throttling(client)
            return await function(*args, **kwargs)

    return wrapper
