# mypy: ignore-errors
"""
Модуль для работы с API OpenSky Network и Nominatim.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import requests
import time


class BaseAPI(ABC):
    """Абстрактный класс для работы с API."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    @abstractmethod
    def _connect(self, endpoint: str, params: Dict[str, Any]) -> Any:
        """Приватный метод для подключения к API."""
        pass

    @abstractmethod
    def get_data(self, country: str) -> List[Dict[str, Any]]:
        """Получение данных с API."""
        pass


class OpenSkyAPI(BaseAPI):
    """Класс для работы с OpenSky Network API."""

    def __init__(self) -> None:
        super().__init__("https://opensky-network.org/api")
        self._nominatim_url = "https://nominatim.openstreetmap.org/search"

    def _connect(self, endpoint: str, params: Dict[str, Any]) -> Any:
        """Приватный метод для подключения к API."""
        url = f"{self._base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_country_bbox(self, country: str) -> Dict[str, float]:
        """Получение bounding box страны через Nominatim."""
        time.sleep(1)

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        params = {
            "q": country,
            "format": "json",
            "limit": 1
        }
        response = requests.get(
            self._nominatim_url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError(f"Страна '{country}' не найдена")

        bbox = data[0]["boundingbox"]
        return {
            "lamin": float(bbox[0]),
            "lamax": float(bbox[1]),
            "lomin": float(bbox[2]),
            "lomax": float(bbox[3])
        }

    def get_data(self, country: str) -> List[Dict[str, Any]]:
        """Получение списка самолётов над указанной страной."""
        bbox = self._get_country_bbox(country)
        params = {
            "lamin": bbox["lamin"],
            "lamax": bbox["lamax"],
            "lomin": bbox["lomin"],
            "lomax": bbox["lomax"]
        }
        data = self._connect("states/all", params)  # type: ignore[arg-type]
        return data.get("states", [])
