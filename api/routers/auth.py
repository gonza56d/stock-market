"""API Router with endpoints related to authentication."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.business.auth import AuthBusiness
from api.repositories.exceptions import NotFound

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.get('/')
async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        user_id = AuthBusiness().get_user_id(token)
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user_id
