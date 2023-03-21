"""API Router with endpoints related to operations with users."""
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from api.business.exceptions import EmailTaken
from api.business.users import UsersBusiness
from api.models.users import UserSignUp

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/sign_up', status_code=201)
async def sign_up(user_sign_up: UserSignUp):
    try:
        UsersBusiness().create_user(user_sign_up)
    except EmailTaken:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email already taken',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return {}
