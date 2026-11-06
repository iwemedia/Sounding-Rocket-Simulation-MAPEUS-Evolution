# ===================
# models/mission.py
# ==================

"""

Tracks the active state, phase progression, and operational flags
of the ongoing suborbital simulation campaign.

"""


class Mission:
    """
    Architectural state container that isolates campaign phase progression
    from the central control flow orchestrator.

    """

    def __init__(self):
        # self.current_phase: describes the global, excact state of mission in the memory
        # starts strictly at Phase 0 (Welcome Screen baseline configuration)
        self.current_phase = 0

        # self.is-valid_mission: is a boolean safty flag - it acts as Go/NoGo dashboard matrix indicator
        self.is_valid_mission = True

    def advance_phase(self):
        """Increments the campaign phase tracker chronologically."""
        self.current_phase += 1

    def invalidate_mission(self):
        """Hard trigger to scrub operations if environmental bounds are violated."""
        self.is_valid_mission = False
