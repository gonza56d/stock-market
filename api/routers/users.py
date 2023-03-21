"""API Router with endpoints related to operations with users."""
from fastapi import APIRouter

from api.business.users import UsersBusiness
from api.models.users import UserSignUp

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/sign_up', status_code=201)
async def sign_up(user_sign_up: UserSignUp):
    UsersBusiness().create_user(user_sign_up)
    return {}
