# ==========================================
#  physics/__init__.py
# ==========================================

"""
Physics engine package housing stateless analytical engineering formulas.
"""

from physics.mass_properties_calculator import calculate_total_mass, calculate_total_inertia
from physics.de_spin_calculator import calculate_despin_mass

# Facade interface for the controller layer
__all__ = [
    "calculate_total_mass",
    "calculate_total_inertia",
    "calculate_despin_mass"
]
