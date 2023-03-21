from httpx import AsyncClient

from api.env import Env
from api.models.stock_market import SymbolOption, FunctionOption


class StockMarketRepository:
    """HTTP Repository of the main functionality using alphavantage"""

    def __init__(self):
        self._base_url = 'https://www.alphavantage.co/query'
        self._request_client = AsyncClient()
        self._api_key = Env.ALPHAVANTAGE_API_KEY

    async def get(self, symbol: SymbolOption, function: FunctionOption):
        async with self._request_client as request:
            response = await request.get(
                self._base_url,
                params={
                    'symbol': symbol.alphavantage_value(),
                    'function': function.alphavantage_value(),
                    'apikey': self._api_key
                },
            )
        return response.json()
