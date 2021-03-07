import json

import httpx
from tenacity import retry, wait_exponential, stop_after_attempt


class APIClass:

    _session: httpx.AsyncClient = None

    _headers = None

    def __init__(self, access_token: str = None):
        self._headers: dict = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
        }
        if access_token is not None:
            self._headers['Authorization'] = access_token

    @property
    def _client_session(self) -> httpx.AsyncClient:
        if not self._session or self._session.is_closed:
            self._session = httpx.AsyncClient(headers=self._headers)

        return self._session

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=2),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def make_request(self, method: str, url: str, payload: dict = None):
        request = httpx.Request(method, url, headers=self._headers, json=payload)
        response = await self._client_session.send(request)

        return self._check_result(request, response)

    @staticmethod
    def _check_result(request: httpx.Request, response: httpx.Response):
        if response.status_code != 200:
            raise httpx.HTTPStatusError("Error status_code", request=request, response=response)

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise httpx.DecodingError("Error decode to json", request=request)
