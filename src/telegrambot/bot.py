import abc
import json
import requests
from typing import Union


class FakeResponse:
    pass


class AbstractBot(abc.ABC):

    def __init__(self, token: str, name: str = ""):
        self._token = token
        self.name = name
        self._base_url = f"https://api.telegram.org/bot{self._token}/"

    @property
    def token(self) -> str:
        return self._token

    def get_updates(self) -> tuple[bool, int, dict[str, any]]:
        """ Get updates for the current bot.
        """
        url = self._base_url + "getUpdates?timeout=100"
        res = self._get_request(url)
        content = {}
        if res.ok:
            content = json.loads(res.content)
        return res.ok, res.status_code, content

    @abc.abstractmethod
    def _post_request(self, url: str, *args) -> Union[requests.Response, FakeResponse]:
        pass

    @abc.abstractmethod
    def _get_request(self, url: str, *args) -> Union[requests.Response, FakeResponse]:
        pass


class TelegramBot(AbstractBot):
    """ Class to interact with the telegram bot API.
    """

    def _post_request(self, url: str, *args) -> requests.Response:
        pass

    def _get_request(self, url: str, *args) -> requests.Response:
        pass


class TestBot(AbstractBot):
    """ Class used for testing purposes. Doesn't send requests
        to telegram API.
    """

    def _post_request(self, url: str, *args) -> FakeResponse:
        pass

    def _get_request(self, url: str, *args) -> FakeResponse:
        pass
