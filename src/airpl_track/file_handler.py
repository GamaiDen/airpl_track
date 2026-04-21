import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from airpl_track.aeroplane import Aeroplane


class BaseFileHandler(ABC):
    """Абстрактный класс для сохранения данных."""

    @abstractmethod
    def add(self, aeroplane: Aeroplane) -> None:
        """Добавление самолёта."""
        pass

    @abstractmethod
    def get(self, criteria: Dict[str, Any]) -> List[Aeroplane]:
        """Получение самолётов по критериям."""
        pass

    @abstractmethod
    def delete(self, criteria: Dict[str, Any]) -> None:
        """Удаление самолётов по критериям."""
        pass


class JSONFileHandler(BaseFileHandler):
    """Класс для работы с JSON-файлами."""

    def __init__(self, filename: str = "aeroplanes.json") -> None:
        self._filename = filename
        # Создаем файл с пустым списком, если его нет или он пустой
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f)
        else:
            # Проверяем, что файл не пустой
            try:
                with open(self._filename, "r", encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError:
                with open(self._filename, "w", encoding="utf-8") as f:
                    json.dump([], f)

    def _read_all(self) -> List[Dict[str, Any]]:
        """Чтение всего файла."""
        with open(self._filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _write_all(self, data: List[Dict[str, Any]]) -> None:
        """Запись в файл."""
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, aeroplane: Aeroplane) -> None:
        """Добавление самолёта без дубликатов."""
        data = self._read_all()
        aeroplane_dict = aeroplane.to_dict()
        if aeroplane_dict not in data:
            data.append(aeroplane_dict)
            self._write_all(data)

    def get(self, criteria: Dict[str, Any]) -> List[Aeroplane]:
        """Получение самолётов по критериям."""
        data = self._read_all()
        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                # Создаем объект Aeroplane из словаря
                aeroplane = Aeroplane(
                    icao24=item["icao24"],
                    callsign=item["callsign"],
                    origin_country=item["origin_country"],
                    longitude=item.get("longitude"),
                    latitude=item.get("latitude"),
                    velocity=item.get("velocity"),
                    altitude=item.get("altitude")
                )
                result.append(aeroplane)
        return result

    def delete(self, criteria: Dict[str, Any]) -> None:
        """Удаление самолётов по критериям."""
        data = self._read_all()
        new_data = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if not match:
                new_data.append(item)
        self._write_all(new_data)
