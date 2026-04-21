import pytest
from airpl_track.aeroplane import Aeroplane


@pytest.fixture
def sample_aeroplane():
    """Тестовый самолёт."""
    return Aeroplane(
        icao24="abc123",
        callsign="AFL123",
        origin_country="Russia",
        longitude=37.6,
        latitude=55.7,
        velocity=250.0,
        altitude=10000.0
    )


@pytest.fixture
def sample_aeroplane_list():
    """Список тестовых самолётов."""
    return [
        Aeroplane("icao1", "CALL1", "Russia", 10.0, 20.0, 200.0, 10000.0),
        Aeroplane("icao2", "CALL2", "USA", 15.0, 25.0, 220.0, 12000.0),
        Aeroplane("icao3", "CALL3", "Russia", 12.0, 22.0, 180.0, 8000.0),
        Aeroplane("icao4", "CALL4", "Germany", 18.0, 28.0, 250.0, None),
    ]
