# physics/mass_properties_calculator.py

from config.constants import (
    ROCKET_BASE_MASS,
    ROCKET_BASE_INERTIA,
    INERTIA_PER_BIO,
    INERTIA_PER_TEC,
)

def calculate_total_mass(payload_masses: list[float]) -> float:
    """
    Sums up module masses and factors in the structural base vehicle mass.
    """
    mass_payload_configuration = sum(payload_masses)
    return ROCKET_BASE_MASS + mass_payload_configuration

def calculate_total_inertia(bio_count: int, tec_count: int) -> float:
    """
    Applies structural formulas to compute the total system inertia.
    """
    i_experiments = (bio_count * INERTIA_PER_BIO) + (tec_count * INERTIA_PER_TEC)
    return ROCKET_BASE_INERTIA + i_experiments