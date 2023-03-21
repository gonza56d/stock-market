"""API Router with endpoints related to authentication."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.business.auth import AuthBusiness
from api.business.exceptions import InvalidCredentials
from api.models.auth import Auth, AuthToken
from api.repositories.exceptions import NotFound

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.get('/')
async def get_current_user_email(token: Annotated[str, Depends(oauth2_scheme)]):
    """Validate session token against cache and return user email."""
    try:
        email = AuthBusiness().validate_token(token)
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid auth token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return email


@router.post('/', response_model=AuthToken, status_code=201)
async def authenticate(credentials: Auth):
    """Validate user credentials and return session token."""
    try:
        access_token = AuthBusiness().authenticate(credentials)
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return access_token
