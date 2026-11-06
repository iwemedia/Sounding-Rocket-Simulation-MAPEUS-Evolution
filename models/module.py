# models/module.py
"""
this class represents a single scientific or technological experiment slot on the production bench, mapping
directly to the catalog data parameters.

Attributes:
        key (str): Unique shorthand identifier from the catalog (e.g., 'bio1').
        instance_id (str): Unique runtime identifier on the bench (e.g., 'BIO-01').
        type (str): The payload category, restricted to 'Bio' or 'Tec'.
        name (str): clear  text string to name the experiment.
        description (str): Detailed operational summary of the scientific payload.(60-80 chars recommended)
        mass (float): Total mass metric of the physical module hardware in kg.
"""

class Module:
    def __init__(self, key: str, module_type: str, name: str, description: str, mass: float):
        self.key = key
        self.type = module_type
        self.name = name
        self.description = description
        self.mass = mass
        # id is empty, will be generated while assembling the rocket
        self.instance_id = ""
