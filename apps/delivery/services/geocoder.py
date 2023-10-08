from typing import Optional, List
from abc import ABC, abstractmethod
import requests
import logging


logger = logging.getLogger(__name__)


class Geocoder(ABC):
    def __int__(self, api_key: str):
        self.yandex_geocoder_api_key: str = api_key  # yandex geocoder api key

    @abstractmethod
    def suggestions(self, query: str) -> Optional[List]:
        """ get address suggestions """
        pass

    def address_detail(self, query: str) -> Optional[dict]:
        """ use suggestion query to get address full details """
        base_url = "https://geocode-maps.yandex.ru/1.x/"
        params = {"format": "json", "apikey": self.yandex_geocoder_api_key, "geocode": query}

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            logger.error(f"Error at get_full_address: {response.status_code}")
            return

        data = response.json()
        address_detail = data['response']['GeoObjectCollection']['featureMember'][0]

        return address_detail


class YandexSuggestions(Geocoder):
    def __init__(self, suggestions_api_key: str):
        self.suggestions_api_key: str = suggestions_api_key

    def suggestions(self, query):
        base_url = "https://suggest-maps.yandex.ru/v1/suggest"
        params = {"apikey": self.suggestions_api_key,
                  "text": query,
                  "lang": "ru_RU",
                  "attrs":"uri"}

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            logger.error(f"Error at get suggestions: {response.status_code}")
            return

        result = response.json()["results"]
        suggestions = []
        for suggestion in result:
            title = suggestion["title"]["text"]
            subtitle = suggestion["subtitle"]["text"] if "subtitle" in suggestion.keys() else ""
            # "uri": suggestion["uri"] для точной передачи в геокодер
            info = {"query": f"{subtitle + ', ' if subtitle else ''}{title}"}
            suggestions.append(info)

        return suggestions


class KladrSuggestions(Geocoder):
    def __init__(self, suggestions_api_key: str):
        self.suggestions_api_key: str = suggestions_api_key

    def suggestions(self, query:str):
        base_url = "https://kladr-api.ru/api.php"
        params = {"token": self.suggestions_api_key,
                  "query": query,
                  "withParent": True,
                  "limit": 10,
                  "oneString": 1}

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            logger.error(f"ERROR {response.status_code}: {response.text}")
            return

        result = response.json()["result"]
        suggestions = []
        for suggestion in result:
            info = {"query": suggestion["fullName"]}
            suggestions.append(info)

        return suggestions
