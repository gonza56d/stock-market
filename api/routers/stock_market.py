"""API Router with endpoints related to operations with stock market."""
from typing import Annotated

from fastapi import APIRouter, Depends

from .auth import get_current_user_email
from api.models.users import User

router = APIRouter(
    prefix='/stock-market',
    tags=['stock-market']
)


@router.get('/')
async def test(token: Annotated[User, Depends(get_current_user_email)]):
    """Root endpoint. Requires auth token."""
    return {'user': token}
