"""API Router with endpoints related to operations with stock market."""
from typing import Annotated

from fastapi import APIRouter, Depends, Request

from .auth import require_auth_token
from api.models.users import User
from .throttling import validate_throttling
from ..business.stock_market import StockMarketBusiness
from ..models.stock_market import SymbolOption, FunctionOption, Stock

router = APIRouter(
    prefix='/stock-market',
    tags=['stock-market']
)


@router.get('/', response_model=Stock)
@validate_throttling
async def root(
    token: Annotated[User, Depends(require_auth_token)],
    request: Request,
    symbol: SymbolOption,
    function: FunctionOption
):
    """Root endpoint. Requires auth token."""
    result = await StockMarketBusiness().get_stock_market(symbol, function)
    return result
