"""API Router with endpoints related to operations with stock market."""
from typing import Annotated

from fastapi import APIRouter, Depends

from .auth import require_auth_token
from api.models.users import User

router = APIRouter(
    prefix='/stock-market',
    tags=['stock-market']
)


@router.get('/')
async def root(token: Annotated[User, Depends(require_auth_token)]):
    """Root endpoint. Requires auth token."""
    return {'user': token}
