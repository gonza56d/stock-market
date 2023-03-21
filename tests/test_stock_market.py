from http import HTTPStatus
import responses

from parameterized import parameterized

from api.env import Env
from api.models.auth import Auth
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
        assert 'open_price' in json
        assert 'higher_price' in json
        assert 'lower_price' in json
        assert 'variation' in json

    def test_stock_market_wrong_auth_token(self):
        response = self.client.get(
            '/stock-market',
            params={
                'function': 'DAILY',
                'symbol': 'GOOGLE'
            },
            headers={'Authorization': 'Bearer WRONG.TOKEN'}
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

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @responses.activate
    def test_throttling(self):
        Env.THROTTLING_SECONDS = 1

        # Mock Alpha Vantage API call for faster response in order to test throttling
        responses.add(
            responses.POST,
            'https://www.alphavantage.co/query',
            json={
                'Meta Data': {
                    '1. Information': 'Monthly Adjusted Prices and Volumes',
                    '2. Symbol': 'AAPL',
                    '3. Last Refreshed': '2023-03-20',
                    '4. Time Zone': 'US/Eastern'
                },
                'Monthly Adjusted Time Series': {
                    '2023-03-20': {
                        '1. open': '146.8300',
                        '2. high': '157.8200',
                        '3. low': '143.9000',
                        '4. close': '157.4000',
                        '5. adjusted close': '157.4000',
                        '6. volume': '976003226',
                        '7. dividend amount': '0.0000'
                    },
                }
            }
        )

        for n in range(2):
            response = self.client.get(
                '/stock-market',
                params={
                    'function': 'DAILY',
                    'symbol': 'MICROSOFT'
                },
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )

        assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS
