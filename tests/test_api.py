import pytest
from unittest.mock import patch, MagicMock
from airpl_track.api import OpenSkyAPI


@patch("airpl_track.api.requests.get")
def test_get_country_bbox_success(mock_get):
    """Тест успешного получения bounding box."""
    mock_response = MagicMock()
    mock_response.json.return_value = [{"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = OpenSkyAPI()
    bbox = api._get_country_bbox("Testland")

    assert bbox["lamin"] == 10.0
    assert bbox["lamax"] == 20.0
    assert bbox["lomin"] == 30.0
    assert bbox["lomax"] == 40.0


@patch("airpl_track.api.requests.get")
def test_get_country_bbox_not_found(mock_get):
    """Тест: страна не найдена."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = OpenSkyAPI()
    with pytest.raises(ValueError, match="Страна 'Nowhere' не найдена"):
        api._get_country_bbox("Nowhere")


@patch("airpl_track.api.OpenSkyAPI._get_country_bbox")
@patch("airpl_track.api.OpenSkyAPI._connect")
def test_get_data_success(mock_connect, mock_bbox):
    """Тест успешного получения данных о самолётах."""
    mock_bbox.return_value = {
        "lamin": 10.0, "lamax": 20.0, "lomin": 30.0, "lomax": 40.0
    }
    mock_connect.return_value = {"states": [["icao1", "C1", "RUS"]]}

    api = OpenSkyAPI()
    result = api.get_data("Russia")

    assert len(result) == 1
    assert result[0][0] == "icao1"


@patch("airpl_track.api.OpenSkyAPI._get_country_bbox")
@patch("airpl_track.api.OpenSkyAPI._connect")
def test_get_data_empty(mock_connect, mock_bbox):
    """Тест: пустой ответ от API."""
    mock_bbox.return_value = {
        "lamin": 10.0, "lamax": 20.0, "lomin": 30.0, "lomax": 40.0
    }
    mock_connect.return_value = {}

    api = OpenSkyAPI()
    result = api.get_data("Russia")

    assert result == []
