from tenacity import retry, wait_exponential, stop_after_attempt


class BaseClass:

    client = None

    def __init__(self, http_client):
        self.client = http_client


class APIClass(BaseClass):

    headers: dict = None

    def __init__(self, http_client, auth_token: str):
        super().__init__(http_client)
        self.headers = {"Authorization": auth_token}

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=2),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def _rs_get(self, url) -> dict:
        response = await self.client.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=2),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def _rs_post(self, url, data: dict = None) -> dict:
        response = await self.client.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 200

        return response.json()
