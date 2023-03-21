from http import HTTPStatus

from fastapi import HTTPException
from httpx import AsyncClient

from api.env import Env
from api.models.stock_market import SymbolOption, FunctionOption, Stock


class StockMarketRepository:
    """HTTP Repository of the main functionality using alphavantage"""

    def __init__(self):
        self._base_url = 'https://www.alphavantage.co/query'
        self._request_client = AsyncClient()
        self._api_key = Env.ALPHAVANTAGE_API_KEY

    async def get(self, symbol: SymbolOption, function: FunctionOption) -> Stock:
        async with self._request_client as request:
            response = await request.get(
                self._base_url,
                params={
                    'symbol': symbol.alphavantage_value(),
                    'function': function.alphavantage_value(),
                    'apikey': self._api_key
                },
            )
        self.validate(response)
        stock = self.process(response)
        return stock

    def validate(self, response):
        if 'Note' in response.json():  # Alpha Vantage API gives 200 even on max calls.
            raise HTTPException(
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                detail='Maximum requests reached for Alpha Vantage API.'
            )

    def process(self, response):
        json = response.json()
        keys = [k for k in json]
        payload: dict = json[keys[1]]

        last_key = [k for k in payload][0]
        open = float(payload[last_key]['1. open'])

        try:
            higher = max([float(value['2. high']) for value in payload.values()])
        except ValueError:
            higher = 0.0

        try:
            lower = min([float(value['3. low']) for value in payload.values()])
        except ValueError:
            lower = 0.0

        variation = None
        if len(payload) >= 2:
            last = payload[[k for k in payload.keys()][0]]
            previous = payload[[k for k in payload.keys()][1]]
            variation = float(previous['4. close']) - float(last['4. close'])

        return Stock(
            open_price=open,
            higher_price=higher,
            lower_price=lower,
            variation=variation
        )
