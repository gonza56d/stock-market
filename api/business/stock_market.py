from api.models.stock_market import SymbolOption, FunctionOption
from api.repositories.stock_market import StockMarketRepository


class StockMarketBusiness:

    def __init__(self):
        self.repository = StockMarketRepository()

    async def get_stock_market(self, symbol: SymbolOption, function: FunctionOption):
        return await self.repository.get(symbol, function)
