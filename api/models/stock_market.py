from enum import Enum

from pydantic import BaseModel


class SymbolOption(str, Enum):

    META = 'META'
    APPLE = 'APPLE'
    MICROSOFT = 'MICROSOFT'
    GOOGLE = 'GOOGLE'
    AMAZON = 'AMAZON'

    def alphavantage_value(self) -> str:
        return {
            SymbolOption.META: 'META',
            SymbolOption.APPLE: 'AAPL',
            SymbolOption.MICROSOFT: 'MSFT',
            SymbolOption.GOOGLE: 'GOOGL',
            SymbolOption.AMAZON: 'AMZN'
        }[self]


class FunctionOption(str, Enum):

    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'

    def alphavantage_value(self) -> str:
        return {
            FunctionOption.DAILY: 'TIME_SERIES_DAILY_ADJUSTED',
            FunctionOption.WEEKLY: 'TIME_SERIES_WEEKLY_ADJUSTED',
            FunctionOption.MONTHLY: 'TIME_SERIES_MONTHLY_ADJUSTED'
        }[self]


class Stock(BaseModel):

    open_price: float
    higher_price: float
    lower_price: float
    variation: float
