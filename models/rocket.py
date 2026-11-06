# models/rocket.py

from typing import List, Optional
from models.module import Module

# Import mathematical functions directly from the physics layer
from physics.mass_properties_calculator import calculate_total_mass, calculate_total_inertia

# Architectural configuration imports
from config.constants import (
    MAX_PAYLOAD_SLOTS,
    MAX_WORKBENCH_SLOTS
)


class Rocket:
    """
    Tracks the active state of the sounding rocket simulation payload configuration.
    Manages module arrays and provides real-time mathematical configuration updates.
    State container -> math and physics delegated to layer physics
    """

    def __init__(self):

        # Dynamically compute total temporary workbench capacity to avoid hardcoded constants
        self.total_assembly_capacity = MAX_WORKBENCH_SLOTS

        # Encapsulated payload stack per rocket instance; stores Module objects with all properties
        # workbench tracking state shifts
        self.modules: List[Optional[Module]] = [None] * self.total_assembly_capacity

        # Guard flag: Physics calculations are locked until the payload assembly is fully finalized
        self.is_finalized = False

    def generate_next_instance_id(self, module_type: str) -> str:
        """
        Generates a non-duplicating unique ID for a given module type.
        Simply finds the highest active sequence number and increments it by 1.

        Args:
            module_type (str): The category of the module ('Bio' or 'Tec').

        Returns:
            str: The unique generated instance ID (e.g., 'BIO-01', 'TEC-02').
        """


        # ID-Prefix-Constructor "Bio" = "BIO" for ID-Construction
        prefix = module_type.upper()

        # Extract all numbers currently in use for this specific type
        active_numbers = []

        for module in self.modules:
            if module is not None and module.type == module_type:
                try:
                    num = int(module.instance_id.split("-")[-1])
                    active_numbers.append(num)
                except (IndexError, ValueError):
                    pass

        next_number = max(active_numbers) + 1 if active_numbers else 1
        return f"{prefix}-{next_number:02d}"


    @property
    def occupied_slots_count(self) -> int:
        """Returns the actual number of modules currently installed on the expanded bench."""
        return sum(1 for module in self.modules if module is not None)


    def add_module_to_slot(self, module: Module, requested_slot: int) -> bool:
        """
        Places a module onto a specific workbench slot, shifting to the next free
        buffer slot if occupied. Preserves gaps for the engineer's layout til finished signal.
        """
        # Guard the strict maximum flight module constraint
        if self.occupied_slots_count >= MAX_PAYLOAD_SLOTS:
            return False

        target_index = requested_slot - 1
        # Clamp bounds safety check against the total expanded capacity
        if target_index < 0:
            target_index = 0
        if target_index >= self.total_assembly_capacity:
            target_index = self.total_assembly_capacity - 1

        # If chosen slot is free, occupy it directly
        if self.modules[target_index] is None:
            self.modules[target_index] = module
            return True

        # Shifting Logic within the expanded buffer zone
        for i in range(target_index + 1, self.total_assembly_capacity):
            if self.modules[i] is None:
                self.modules[i] = module
                return True
        for i in range(target_index - 1, -1, -1):
            if self.modules[i] is None:
                self.modules[i] = module
                return True

        return False


    def remove_module_by_instance_id(self, instance_id: str) -> bool:
        """Finds a module by its tracking ID and clears its workbench position."""
        target_id = instance_id.strip().upper()
        for index, module in enumerate(self.modules):
            if module is not None and module.instance_id == target_id:
                self.modules[index] = None
                return True
        return False



    def finalize_and_close_gaps(self):
        """
        Closes all intentional workbench gaps, compacts the payload deck.
        The flight configuration strictly contains only the installed hardware modules.
        Unlocks the core rocket physics calculations. (is_finalize = True)

        Raises:
            ValueError: If payload configuration violates critical physical constraints
                        (empty payload stack or exceeding max payload slots).

        """
        # Extract all active hardware modules, discarding the empty assembly gaps
        # 1 to MAX_PAYLOAD_SLOTS is allowed. This list will have exactly that chosen length.
        active_modules = [mod for mod in self.modules if mod is not None]

        # physical check for hardware boundaries
        ## empty slot
        if len(active_modules) < 1:
            raise ValueError(
                "Payload Error: Assembly cannot be finalized. "
                "Sounding rockets require at least 1 active scientific module to launch."
            )

        ## > MAX_PAYLOAD_SLOTS:
        if len(active_modules) > MAX_PAYLOAD_SLOTS:
            raise ValueError(
                f"Payload Error: Assembly exceeds maximum physical payload deck capacity. "
                f"Cannot pack {len(active_modules)} modules into {MAX_PAYLOAD_SLOTS} flight slots. "
            )

        #Apply to flight deck configuration
        self.modules = active_modules

        # Flip the architectural safety switch to True
        self.is_finalized = True

    # ==========================================
    # DELEGATING PROPERTIES (State , no math)
    # =========================================***

    @property
    def total_mass(self) -> float:
        """Calculates total rocket mass dynamically. Guarded by finalization check."""
        if not self.is_finalized:
            raise ValueError("Physics error: Mass cannot be calculated while payload assembly is active and open.")

        payload_masses = [module.mass for module in self.modules]
        return calculate_total_mass(payload_masses)

    @property
    def total_inertia(self) -> float:
        """Fetches dynamic system inertia from the physics engine if finalized."""
        if not self.is_finalized:
            raise ValueError("Physics error: Inertia cannot be calculated during open assembly.")

        # Direct call to the standalone function
        return calculate_total_inertia(self.bio_count, self.tec_count)

    @property
    def bio_count(self) -> int:
        return sum(1 for m in self.modules if m is not None and m.type == "Bio")

    @property
    def tec_count(self) -> int:
        return sum(1 for m in self.modules if m is not None and m.type == "Tec")

    @property
    def active_instance_ids(self) -> list[str]:
        #loop runs through ever slot at the bench, m is the actual module at that slot
        # grabs ID-string if: filtert 'if not None' (has to be a module not empty at that spot)
        return [m.instance_id for m in self.modules if m is not None]