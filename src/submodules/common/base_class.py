import json

import httpx
from tenacity import retry, wait_fixed, stop_after_attempt


class APIClass:

    _session: httpx.AsyncClient = None

    _headers = None

    def __init__(self, access_token: str = None):
        self._headers: dict = {
            # "Accept": "application/json",
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
        wait=wait_fixed(1),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def make_request(self, method: str, url: str, payload: dict = None):
        request = httpx.Request(method, url, headers=self._headers, json=payload)
        response = await self._client_session.send(request)

        return self._check_result(request, response)

    async def send_file(self, method: str, url: str, data):
        self._headers['Content-Type'] = "multipart/form-data"

        request = httpx.Request(method, url, headers=self._headers, data=data)
        response = await self._client_session.send(request)

        return self._check_result(request, response)

    @staticmethod
    def _check_result(request: httpx.Request, response: httpx.Response):
        if response.status_code != 200:
            raise httpx.HTTPStatusError(
                f"Error status_code: {response.text}",
                request=request,
                response=response
            )

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise httpx.DecodingError("Error decode to json", request=request)
