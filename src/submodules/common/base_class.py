
class BaseClass:

    client = None

    def __init__(self, http_client):
        self.client = http_client


class APIClass(BaseClass):

    headers: dict = None

    def __init__(self, http_client, auth_token: str):
        super().__init__(http_client)
        self.headers = {"Authorization": auth_token}

    async def _rs_get(self, url) -> dict:
        response = await self.client.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()

    async def _rs_post(self, url, data: dict = None) -> dict:
        response = await self.client.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 200

        return response.json()