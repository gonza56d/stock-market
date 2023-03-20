"""API Router with endpoints related to authentication."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.business.auth import AuthBusiness

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.get('/')
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = AuthBusiness().get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user
