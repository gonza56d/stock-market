"""API Router with endpoints related to authentication."""

from fastapi import APIRouter


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.get('/')
async def test():
    return {'hello': 'world'}
