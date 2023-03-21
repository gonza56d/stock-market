"""API Router with endpoints related to operations with stock market."""
from typing import Annotated

from fastapi import APIRouter, Depends

from .auth import require_auth_token
from api.models.users import User
from ..business.stock_market import StockMarketBusiness
from ..models.stock_market import SymbolOption, FunctionOption

router = APIRouter(
    prefix='/stock-market',
    tags=['stock-market']
)


@router.get('/')
async def root(
    token: Annotated[User, Depends(require_auth_token)],
    symbol: SymbolOption,
    function: FunctionOption
):
    """Root endpoint. Requires auth token."""
    result = await StockMarketBusiness().get_stock_market(symbol, function)
    return result
