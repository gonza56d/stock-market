"""API Router with endpoints related to operations with stock market."""

from fastapi import APIRouter


router = APIRouter(
    prefix='/stock-market',
    tags=['stock-market']
)


@router.get('/')
async def test():
    return {'hello': 'world'}
