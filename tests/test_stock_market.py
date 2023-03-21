from http import HTTPStatus

from parameterized import parameterized

from api.models.auth import Auth
from api.models.stock_market import SymbolOption
from api.models.users import User
from api.repositories.auth import AuthRepository, AccessTokenRepository
from api.repositories.users import UsersRepository
from tests import ApiTest


class TestStockMarket(ApiTest):

    payload_key = {
        'DAILY': 'Time Series (Daily)',
        'WEEKLY': 'Weekly Adjusted Time Series',
        'MONTHLY': 'Monthly Adjusted Time Series'
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
        ('META', 'DAILY'),
        ('APPLE', 'WEEKLY'),
        ('MICROSOFT', 'MONTHLY'),
        ('GOOGLE', 'DAILY'),
        ('AMAZON', 'WEEKLY'),
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
        assert json['Meta Data']['2. Symbol'] == (
            SymbolOption(symbol).alphavantage_value()
        )
        assert isinstance(json[self.payload_key[function]], dict)

        for result in json[self.payload_key[function]].values():
            assert '1. open' in result.keys()
            assert '2. high' in result.keys()
            assert '3. low' in result.keys()

    def test_stock_market_wrong_auth_token(self):
        response = self.client.get(
            '/stock-market',
            params={
                'function': 'DAILY',
                'symbol': 'GOOGLE'
            },
            headers={'Authorization': f'Bearer WRONG.TOKEN'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @parameterized.expand([
        ('DAILY', 'SOME_INVALID_SYMBOL'),
        ('SOME_INVALID_FUNCTION', 'MICROSOFT'),
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
