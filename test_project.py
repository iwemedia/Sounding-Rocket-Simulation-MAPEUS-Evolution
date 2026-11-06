import os
import json
from unittest.mock import patch
from project import (
    calculate_rocket_configuration,
    extract_wind_speed,
    archive_mission_data,
    DEFAULT_WIND_SPEED,
    run_despin_quiz,
)

def test_calculate_rocket_configuration():
    # Testet mit 2 Bio- und 1 Tech-Modul
    i_base, i_exp, i_total, m_bio, m_tec, m_rock = calculate_rocket_configuration(2, 1)

    #happy test
    assert i_base == 1.50
    assert i_exp == 1.00
    assert i_total == 2.50
    assert m_bio == 29.0
    assert m_tec == 29.0
    assert m_rock == 143.0

def test_run_despin_quiz_edge_cases():
    # Cornerstones: simulate wire length: to short, to long, ok
    inputs = ["0.50", "4.00", "2.00"]

    # with patch from modul unittest.mock simulating user input
    with patch("builtins.input", side_effect=inputs), patch("project.console.print"):

        result = run_despin_quiz(2.00)
        assert result == 0.25


def test_extract_wind_speed():
    # Test API-Data correct
    mock_data = {"current": {"wind_speed_10m": 15.5}}
    assert extract_wind_speed(mock_data) == 15.5

    # test fallback
    assert extract_wind_speed({}) == DEFAULT_WIND_SPEED

def test_extract_wind_speed_malformed_data():
    bad_data = {"current": {"wind_speed_10m": "STORM"}}
    assert extract_wind_speed(bad_data) == DEFAULT_WIND_SPEED

    broken_json = {"invalid_key": 42}
    assert extract_wind_speed(broken_json) == DEFAULT_WIND_SPEED


def test_archive_mission_data():
    dummy_dict = {"roms": ("Bio", "ROMS", "Desc", 14.5)}

    # make file function -> JSON in mission_archive
    filepath = archive_mission_data(["roms"], dummy_dict, 12.5)

    # file exists
    assert os.path.exists(filepath)

    with open(filepath, "r") as f:
        data = json.load(f)
        assert data["environmental_conditions"]["wind_speed_kmh"] == 12.5
        assert data["payload_manifest"]["deployed_experiments"] == ["ROMS"]