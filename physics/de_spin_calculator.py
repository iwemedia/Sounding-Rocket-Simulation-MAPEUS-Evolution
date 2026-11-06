# ##################################
#   physics/de_spin_calculator.py
# ##################################
"""
Physics engine for the Yo-Yo De-Spin System and Rocket Configurations.
Inspired by the MORABA MAPHEUS Mission - Germany.
"""

# Import the newly outsourced constants from our configuration facade
from config.constants import (
    MIN_WIRE_LENGTH,
    MAX_WIRE_LENGTH,
)

def calculate_despin_mass(i_total: float, lengths_despin: float) -> float:
    """
    Calculates the required mass per Yo-Yo counterweight based on total inertia
    and chosen wire length in the range of predefined cornerstones physics .
    Returns: half despin_mass in [kg].

    Raises:
        ValueError: If wire length violates the pre-defined physical cornerstones.
    """

    # guard physical corner stones
    if lengths_despin < MIN_WIRE_LENGTH or lengths_despin > MAX_WIRE_LENGTH:
        raise ValueError(
            f"Physical cornerstone violation: Wire length {lengths_despin}m "
            f"must be between {MIN_WIRE_LENGTH}m and {MAX_WIRE_LENGTH}m."
        )

    # calculate de-spin mass in total - (needs to be seperated in two equal weights on two wires)
    despin_mass = round((i_total / (lengths_despin ** 2))/2, 2)
    return despin_mass
