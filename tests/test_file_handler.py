import os
import tempfile
from airpl_track.file_handler import JSONFileHandler
from airpl_track.aeroplane import Aeroplane


def test_json_handler_add_and_get(sample_aeroplane):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        filename = f.name

    handler = JSONFileHandler(filename)
    handler.add(sample_aeroplane)

    result = handler.get({"icao24": "abc123"})
    assert len(result) == 1

    os.unlink(filename)


def test_json_handler_no_duplicates(sample_aeroplane):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        filename = f.name

    handler = JSONFileHandler(filename)
    handler.add(sample_aeroplane)
    handler.add(sample_aeroplane)

    result = handler.get({})
    assert len(result) == 1

    os.unlink(filename)
