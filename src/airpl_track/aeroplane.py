from typing import Any, Dict, List, Optional


class Aeroplane:
    """Класс, представляющий воздушное судно."""

    __slots__ = ("_icao24", "_callsign", "_origin_country", "_longitude", "_latitude", "_velocity", "_altitude")

    def __init__(
        self,
        icao24: str,
        callsign: Optional[str],
        origin_country: str,
        longitude: Optional[float],
        latitude: Optional[float],
        velocity: Optional[float],
        altitude: Optional[float]
    ) -> None:
        self._icao24 = icao24
        self._callsign = self._validate_callsign(callsign)
        self._origin_country = origin_country
        self._longitude = longitude
        self._latitude = latitude
        self._velocity = self._validate_positive(velocity, "Velocity")
        self._altitude = self._validate_positive(altitude, "Altitude")

    def _validate_callsign(self, callsign: Optional[str]) -> str:
        """Валидация позывного."""
        return callsign.strip() if callsign else "N/A"

    def _validate_positive(self, value: Optional[float], name: str) -> Optional[float]:
        """Валидация неотрицательных значений."""
        if value is not None and value < 0:
            return None  # Игнорируем некорректные данные
        return value

    @property
    def icao24(self) -> str:
        return self._icao24

    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @property
    def altitude(self) -> Optional[float]:
        return self._altitude

    @property
    def velocity(self) -> Optional[float]:
        return self._velocity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._altitude == other._altitude

    def __lt__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self._altitude is None or other._altitude is None:
            return False
        return self._altitude < other._altitude

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в словарь."""
        return {
            "icao24": self._icao24,
            "callsign": self._callsign,
            "origin_country": self._origin_country,
            "longitude": self._longitude,
            "latitude": self._latitude,
            "velocity": self._velocity,
            "altitude": self._altitude
        }

    @classmethod
    def from_list(cls, data: List[Any]) -> "Aeroplane":
        """Создание объекта из списка (формат OpenSky)."""
        return cls(
            icao24=data[0],
            callsign=data[1],
            origin_country=data[2],
            longitude=data[5],
            latitude=data[6],
            velocity=data[9],
            altitude=data[7]
        )

    @classmethod
    def cast_to_object_list(cls, raw_data: List[List[Any]]) -> List["Aeroplane"]:
        """Преобразование списка списков в список объектов."""
        return [cls.from_list(item) for item in raw_data]

    def __repr__(self) -> str:
        return f"Aeroplane({self._callsign}, {self._origin_country}, Alt: {self._altitude})"
