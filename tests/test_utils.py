from airpl_track.utils import (
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude,
    get_top_by_altitude,
)


def test_filter_by_country(sample_aeroplane_list):
    result = filter_aeroplanes_by_country(sample_aeroplane_list, ["Russia"])
    assert len(result) == 2


def test_filter_by_country_empty(sample_aeroplane_list):
    result = filter_aeroplanes_by_country(sample_aeroplane_list, [])
    assert len(result) == 4


def test_filter_by_altitude(sample_aeroplane_list):
    result = filter_aeroplanes_by_altitude(sample_aeroplane_list, 9000.0, 11000.0)
    assert len(result) == 1


def test_get_top_by_altitude(sample_aeroplane_list):
    result = get_top_by_altitude(sample_aeroplane_list, 2)
    assert len(result) == 2
    assert result[0].altitude == 12000.0
