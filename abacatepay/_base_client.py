import requests
from typing import Literal
from ._constants import USER_AGENT
from .utils._exceptions import raise_for_status, APITimeoutError, APIConnectionError


class BaseClient:
    def __init__(self, api_key: str):
        self.__api_key = api_key

    def _request(
        self,
        url: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET",
        **kwargs,
    ):
        request = requests.Request(
            method,
            url,
            headers={
                "Authorization": f"Bearer {self.__api_key}",
                "User-Agent": USER_AGENT,
            },
            **kwargs,
        )
        try:
            prepared_request = request.prepare()
            with requests.Session() as s:
                response = s.send(prepared_request)

            raise_for_status(response)
            return response

        except requests.exceptions.Timeout:
            raise APITimeoutError(request=request)

        except requests.exceptions.ConnectionError:
            raise APIConnectionError(message="Connection error.", request=request)
