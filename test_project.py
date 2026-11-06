# test_project.py
"""
Automated unit testing suite for the MAPEUS suborbital campaign simulator.
Validates math property calculators, physics boundary guards, and API contract fallbacks.

Execute via terminal using: pytest test_project.py
"""

import os
import pytest

# Target domain and service imports for isolated logic testing
from physics.mass_properties_calculator import calculate_total_mass, calculate_total_inertia
from physics.de_spin_calculator import calculate_despin_mass
from services import weather_service
from services import archive_service
from models.rocket import Rocket
from models.module import Module


def test_calculate_total_mass():
    """Asserts happy-path mass aggregation factoring in the structural base vehicle mass."""
    # Base vehicle mass is 85.0 kg. Payload masses sum up to 58.0 kg.
    payload_sample = [14.5, 14.5, 29.0]
    expected_total = 85.0 + sum(payload_sample)

    assert calculate_total_mass(payload_sample) == expected_total


def test_calculate_total_inertia():
    """Asserts accurate integration of biological and technological experiment moments of inertia."""
    # Base inertia: 1.50 | Bio multiplier: 0.25 | Tec multiplier: 0.50
    bio_count = 2
    tec_count = 1
    expected_inertia = 1.50 + (bio_count * 0.25) + (tec_count * 0.50)

    assert calculate_total_inertia(bio_count, tec_count) == expected_inertia


def test_calculate_despin_mass_validation():
    """Asserts that physics engine guards successfully validate wire lengths inside allowable boundaries."""
    i_total_sample = 2.50

    # Happy path: length within nominal 0.80m to 3.00m NASA boundaries
    valid_length = 2.00
    expected_mass = round((i_total_sample / (valid_length ** 2)) / 2.0, 2)
    assert calculate_despin_mass(i_total_sample, valid_length) == expected_mass

    # Edge Case: Under minimum wire length cornerstone constraint (0.80m)
    with pytest.raises(ValueError) as error_under:
        calculate_despin_mass(i_total_sample, 0.50)
    assert "Physical cornerstone violation" in str(error_under.value)

    # Edge Case: Exceeding maximum physical layout clearance constraints (3.00m)
    with pytest.raises(ValueError) as error_over:
        calculate_despin_mass(i_total_sample, 4.00)
    assert "Physical cornerstone violation" in str(error_over.value)


def test_extract_wind_speed_nominal():
    """Validates accurate data-contract conversion from standard successful API payloads."""
    nominal_api_response = {
        "current": {
            "wind_speed_10m": 14.5
        }
    }
    assert weather_service.extract_wind_speed(nominal_api_response) == 14.5


def test_extract_wind_speed_malformed_fallbacks():
    """Ensures robust silent error-trigger guarding when server contracts return corrupt or missing fields."""
    default_fallback_wind = 12.5  # Centralized DEFAULT_WIND_SPEED standard metric

    # Scenario A: Target metric key missing from internal layer dictionary
    missing_key_payload = {"current": {}}
    assert weather_service.extract_wind_speed(missing_key_payload) == default_fallback_wind

    # Scenario B: Target payload corrupted with invalid alphanumeric string markers
    corrupt_string_payload = {"current": {"wind_speed_10m": "STORM"}}
    assert weather_service.extract_wind_speed(corrupt_string_payload) == default_fallback_wind

    # Scenario C: Completely blank or dropped response package
    empty_payload = {}
    assert weather_service.extract_wind_speed(empty_payload) == default_fallback_wind


def test_archive_mission_file_serialization():
    """Verifies physical file system interactions, validating FAIR-RDM log compliance."""
    # Bootstrap a temporary test execution context container environment
    test_rocket = Rocket()

    # Initialize a valid mock module matching the exact class parameter signature:
    # key, module_type, name, description, mass
    mock_module = Module(
        "roms",
        "Bio",
        "ROMS",
        "Human Stem Cells Test Unit",
        14.5
    )
    mock_module.instance_id = "BIO-01"

    # Safely mount the module onto the structural workbench grid array
    test_rocket.add_module_to_slot(mock_module, 1)
    test_rocket.finalize_and_close_gaps()  # This will now bypass line 135 cleanly!

    test_dir = "test_mission_archive"
    simulated_wind = 18.5

    # Trigger serialization pipeline engine
    generated_path = archive_service.archive_mission(
        rocket_object=test_rocket,
        wind_speed=simulated_wind,
        success=True,
        archive_dir=test_dir
    )

    # Structural OS Assertion audits
    try:
        assert os.path.exists(generated_path)
        assert os.path.isfile(generated_path)
        assert generated_path.endswith(".json")
    finally:
        # Strict context teardown to clean up temporary test files from the workspace
        if os.path.exists(generated_path):
            os.remove(generated_path)
        if os.path.exists(test_dir):
            os.rmdir(test_dir)
