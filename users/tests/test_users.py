from rest_framework.test import APIClient
from rest_framework import status


class TestCreateWallet:
    def test_if_user_is_anonymous_return_401():
        # AAA (Arrange, Act, Assert)
        # Act - Behaviour(sending request to server)
        client = APIClient()
        response = client.post('/wallets/create_wallet/',
                               {'currency': 'Dollar'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
