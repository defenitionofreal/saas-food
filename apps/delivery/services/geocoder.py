from typing import Optional, List
from abc import ABC, abstractmethod
import requests
import logging


logger = logging.getLogger(__name__)


class Geocoder(ABC):

    @abstractmethod
    def suggestions(self, query: str) -> Optional[List]:
        """ get address suggestions """
        pass

    @staticmethod
    def address_detail(yandex_geocoder_api_key: str, query: str) -> dict:
        """ use suggestion query to get address full details """
        base_url = "https://geocode-maps.yandex.ru/1.x/"
        params = {"format": "json",
                  "apikey": yandex_geocoder_api_key,
                  "geocode": query}

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            logger.error(f"Error at get_full_address: {response.status_code}")
            raise Exception  # todo: make custom

        data = response.json()
        address_detail = data['response']['GeoObjectCollection']['featureMember'][0]

        return address_detail

    @staticmethod
    def address_data_after_yandex_geocoder(address_detail: dict) -> dict:
        address_data = address_detail["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]
        address_data_components = address_data["Components"]
        postcode = address_data["postal_code"]
        display_name = address_data["formatted"]
        coordinates = str(address_detail["GeoObject"]["Point"]["pos"]).split(" ")
        lon, lat = coordinates[0], coordinates[1]

        valid_address_data = {
            "country": next((i["name"] for i in address_data_components if
                             i["kind"] == "country"), None),
            "postcode": postcode,
            "display_name": display_name,
            "city": next((i["name"] for i in address_data_components if
                          i["kind"] == "locality"), None),
            "region": next((i["name"] for i in address_data_components if
                            i["kind"] == "province"), None),
            "street": next((i["name"] for i in address_data_components if
                            i["kind"] == "street"), None),
            "building": next((i["name"] for i in address_data_components if
                              i["kind"] == "house"), None),
            "longitude": float(lon),
            "latitude": float(lat)
        }

        return valid_address_data


class YandexSuggestions(Geocoder):
    def __init__(self, suggestions_api_key: str):
        self.suggestions_api_key: str = suggestions_api_key

    def suggestions(self, query):
        base_url = "https://suggest-maps.yandex.ru/v1/suggest"
        params = {"apikey": self.suggestions_api_key,
                  "text": query,
                  "lang": "ru_RU",
                  "attrs": "uri"}

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            logger.error(f"Error at get suggestions: {response.status_code}")
            raise Exception  # todo: make custom

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

    def suggestions(self, query: str) -> list:
        base_url = "https://kladr-api.ru/api.php"
        params = {"token": self.suggestions_api_key,
                  "query": query,
                  "withParent": True,
                  "limit": 10,
                  "oneString": 1}

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            logger.error(f"ERROR {response.status_code}: {response.text}")
            raise Exception  # todo: make custom

        result = response.json()["result"]
        suggestions = []
        for suggestion in result:
            info = {"query": suggestion["fullName"]}
            suggestions.append(info)

        return suggestions
