import httpx
import base64
from uuid import uuid4

from src.core.config import settings

CLIENT = httpx.AsyncClient()


class BaseClass:

    headers: dict = None

    def __init__(self, auth_token: str):
        self.headers = {"Authorization": auth_token}


class Users(BaseClass):

    get_user_url = 'https://api.hubstaff.com/v2/users/me'  # Получение данных о пользователе по токену.

    async def get_user(self) -> dict:
        """Получение пользовательских данных"""
        response = await CLIENT.get(url=self.get_user_url, headers=self.headers)
        assert response.status_code == 200

        return response.json()

    @classmethod
    async def get_auth_token(cls, code: str) -> dict:
        response = await CLIENT.post(
            url=cls.get_auth_token_url(code),
            headers={"Authorization": f"Basic {cls.encode_data_to_base64()}"}
        )
        assert response.status_code == 200

        return response.json()

    @staticmethod
    def encode_data_to_base64() -> str:
        client_data_to_bytes = f'{settings.HUBSTAFF_CLIENT_ID}:{settings.HUBSTAFF_SECRET_KEY}'.encode()
        return base64.b64encode(client_data_to_bytes).decode()

    @staticmethod
    def get_auth_token_url(code: str):
        return "https://account.hubstaff.com/access_tokens" \
                "?grant_type=authorization_code" \
                f"&code={code}" \
                "&redirect_uri=https://google.com"

    @staticmethod
    def get_auth_code_url():
        return f"https://account.hubstaff.com/authorizations/new" \
               f"?client_id={settings.HUBSTAFF_CLIENT_ID}" \
               f"&response_type=code" \
               f"&nonce={str(uuid4())}" \
               f"&redirect_uri=https://google.com" \
               f"&scope=openid hubstaff:read profile tasks:read"
