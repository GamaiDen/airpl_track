import pytest
from airpl_track.aeroplane import Aeroplane


def test_aeroplane_init(sample_aeroplane):
    assert sample_aeroplane.icao24 == "abc123"
    assert sample_aeroplane.callsign == "AFL123"
    assert sample_aeroplane.origin_country == "Russia"
    assert sample_aeroplane.altitude == 10000.0


def test_aeroplane_callsign_validation():
    a = Aeroplane("icao", None, "Russia", 0, 0, 0, 0)
    assert a.callsign == "N/A"


def test_aeroplane_negative_altitude():
    a = Aeroplane("icao", "CALL", "Russia", 0, 0, 0, -100.0)
    assert a.altitude is None


def test_aeroplane_comparison():
    a1 = Aeroplane("icao1", "C1", "RUS", 0, 0, 0, 10000.0)
    a2 = Aeroplane("icao2", "C2", "RUS", 0, 0, 0, 12000.0)
    assert a1 < a2
    assert a1 != a2


def test_aeroplane_to_dict(sample_aeroplane):
    d = sample_aeroplane.to_dict()
    assert d["icao24"] == "abc123"


def test_aeroplane_from_list():
    data = ["icao123", "CALL123", "Russia", 0, 0, 10.0, 20.0, 10000.0, 0, 250.0]
    a = Aeroplane.from_list(data)
    assert a.icao24 == "icao123"
    assert a.altitude == 10000.0


def test_cast_to_object_list():
    raw = [
        ["icao1", "C1", "RUS", 0, 0, 1.0, 2.0, 1000.0, 0, 100.0],
        ["icao2", "C2", "USA", 0, 0, 3.0, 4.0, 2000.0, 0, 200.0],
    ]
    result = Aeroplane.cast_to_object_list(raw)
    assert len(result) == 2
