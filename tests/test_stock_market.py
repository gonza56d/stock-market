from http import HTTPStatus

from parameterized import parameterized

from api.models.auth import Auth
from api.models.users import User
from api.repositories.auth import AuthRepository, AccessTokenRepository
from api.repositories.users import UsersRepository
from tests import ApiTest


class TestStockMarket(ApiTest):

    payload_key = {
        'TIME_SERIES_DAILY_ADJUSTED': 'Time Series (Daily)',
        'TIME_SERIES_WEEKLY_ADJUSTED': 'Weekly Adjusted Time Series',
        'TIME_SERIES_MONTHLY_ADJUSTED': 'Monthly Adjusted Time Series'
    }

    def setUp(self) -> None:
        super().setUp()
        self.email = 'test@test.com'
        self.password = 'somepassword'
        UsersRepository().save(User(
            email=self.email,
            name='John',
            last_name='Rambo'
        ))
        AuthRepository().save(Auth(
            email=self.email,
            password=self.password
        ))
        self.auth_token = AccessTokenRepository().generate_access_token(self.email)

    @parameterized.expand([
        ('META', 'TIME_SERIES_DAILY_ADJUSTED'),
        ('AAPL', 'TIME_SERIES_WEEKLY_ADJUSTED'),
        ('MSFT', 'TIME_SERIES_MONTHLY_ADJUSTED'),
        ('GOOGL', 'TIME_SERIES_DAILY_ADJUSTED'),
        ('AMZN', 'TIME_SERIES_WEEKLY_ADJUSTED'),
    ])
    def test_stock_market_success(self, symbol: str, function: str):
        response = self.client.get(
            '/stock-market',
            params={
                'function': function,
                'symbol': symbol
            },
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert json['Meta Data']['Symbol'] == symbol
        assert isinstance(json[self.payload_key[symbol]], dict)

        for result in json[self.payload_key[symbol]].values():
            assert '1. open' in result.keys()
            assert '2. high' in result.keys()
            assert '3. low' in result.kets()

    def test_stock_market_wrong_auth_token(self):
        response = self.client.get(
            '/stock-market',
            params={
                'function': 'TIME_SERIES_DAILY_ADJUSTED',
                'symbol': 'GOOGL'
            },
            headers={'Authorization': f'Bearer WRONG.TOKEN'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @parameterized.expand([
        ('TIME_SERIES_DAILY_ADJUSTED', 'SOME_INVALID_SYMBOL'),
        ('SOME_INVALID_FUNCTION', 'MSFT'),
        ('SOME_INVALID_FUNCTION', 'SOME_INVALID_SYMBOL')
    ])
    def test_stock_market_wrong_options(self, symbol: str, function: str):
        response = self.client.get(
            '/stock-market',
            params={
                'function': symbol,
                'symbol': function
            },
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
