# controllers/game_controller.py
import sys
import random
import time
from datetime import datetime
from typing import Dict

# Core domain models
from models.rocket import Rocket
from models.module import Module

# Architectural state container for phase progression
from models.mission import Mission

# Presentation layer view
from views.terminal_view import TerminalView

# Architectural simulation services
from services.weather_service import fetch_weather_data, extract_wind_speed
from services import archive_service

# Physical calculations and engines
from physics.de_spin_calculator import calculate_despin_mass

# Global application constants and data registries
from config.catalog import EXPERIMENTS
from config.constants import (
    LAUNCH_SITE_LAT,
    LAUNCH_SITE_LON,
    MAX_ALLOWABLE_WIND_SPEED,
    ROCKET_BASE_INERTIA,
)


class GameController:
    """
    Main orchestration engine (Controller) of the MAPHEUS simulation.
    Drives the chronological campaign pipeline following the MVC pattern.
    Completely decoupled from I/O operations; all user communications
    are delegated to the view component.
    """

    def __init__(self):
        self.rocket = Rocket()
        self.view = TerminalView()
        self.catalog: Dict = EXPERIMENTS

        # SYSTEM DESIGN NOTE (State Pattern Blueprint):
        # Instead of managing the campaign workflow tracking via primitive local integer variables,
        # the logical timeline progression is encapsulated within a dedicated 'Mission' state model.
        # This isolates state-transitions from control-flow and paves the way for future
        # modular mission profile expansions or custom phase injections without modifying the orchestrator.
        self.mission = Mission()

    def start_campaign(self):
        """Starts the campaign pipeline chronologically driven by the Mission state model."""

        # ------- PHASE 0: WELCOME SCREEN & MISSION BRIEFING
        # State Context: Initiates calibration sequence at phase 0 baseline.
        self.run_welcome_phase()
        self.view.render_mission_briefing()

        # Chronological State Transition: Advance from briefing to payload deck construction.
        self.mission.advance_phase()

        # ------- PHASE 1: PAYLOAD ASSEMBLE WORKBENCH
        # State Context: Opens the virtual workbench grid interface (Phase 1).
        self.run_workbench_phase()

        # Chronological State Transition: Advance payload engineering to wire calculations.
        self.mission.advance_phase()

        # ------- PHASE 2: DE-SPIN SYSTEM CALCULATION
        # State Context: Triggers the mathematical validation loop under NASA D-3848 parameters (Phase 2).
        self.run_despin_phase()

        # Chronological State Transition: Advance vehicle engineering to environmental pad assessment.
        self.mission.advance_phase()

        # ------- PHASE 3: LAUNCH PAD WEATHER CHECK
        # State Context: Live REST API meteorological telemetry validation gate (Phase 3).
        wind_speed = self.run_weather_phase()

        # Chronological State Transition: Weather window is nominal -> Advance to ignition and liftoff.
        self.mission.advance_phase()

        # ------- PHASE 4: LAUNCH GRAPHICS & SIMULATION
        # State Context: Animates the real-time asynchronous suborbital flight curve (Phase 4).
        self.run_launch_phase()

        # Chronological State Transition: Vehicle landed safely -> Advance to payload serialization.
        self.mission.advance_phase()

        # ------- PHASE 5: MISSION REPORT & DATA ARCHIVE
        # State Context: Finalizes campaign operations, exports FAIR-compliant JSON logs (Phase 5).
        self.run_archive_phase(wind_speed)

    def run_welcome_phase(self):
        """Manages the startup interface loop and processes bootstrap trigger inputs."""
        self.view.render_welcome_screen()

        # ---- ASK FOR USER INPUT TO START ----
        while True:
            choice = self.view.prompt_for_start()

            if choice == "ESC":
                self.view.clear_screen()
                sys.exit(0)
            elif choice == "START":
                break
            else:
                self.view.render_welcome_screen()


    def run_workbench_phase(self):
        """
        Manages the interactive payload assembly workbench loop until finalized.
        """

        # TASK ASSEMBLING PAYLOAD
        while not self.rocket.is_finalized:
            self.view.render_workbench_interface(self.rocket.modules, self.catalog)
            user_input = self.view.prompt_workbench_action()

            # Action: START / NEXT Task
            if user_input == "next":
                self.handle_finalization_safeguard()

            # Action: REMOVE
            elif user_input.startswith("remove "):
                instance_id = user_input.replace("remove ", "").upper().strip()
                success = self.rocket.remove_module_by_instance_id(instance_id)

                if success:
                    self.view.render_module_removal_success(instance_id)
                else:
                    self.view.render_module_removal_warning(instance_id)

            # Action: ADD EXPERIMENT
            # Checks if Modul is in the Catalog and jumps into the placement function
            elif user_input in self.catalog:
                self.handle_two_stage_placement(user_input)

            # ERROR HANDLING
            else:
                self.view.render_generic_command_error()

        # ==== PLAYER FEEDBACK - REVIEW PHASE 1 MOVE TO PHASE 2
        """
        Render Phase 1: Summary using computed properties from model layer.
        # Replaces old local structural variables: mass_bio_total, mass_tec_total, mass_rocket
        """
        self.view.render_phase_one_complete(
            n_bio=self.rocket.bio_count,
            # implemented "is not None" filters to prevent static analysis warnings
            mass_bio=sum(m.mass for m in self.rocket.modules if m is not None and m.type == "Bio"),

            n_tec=self.rocket.tec_count,
            # implemented "is not None" filters to prevent static analysis warnings
            mass_tec=sum(m.mass for m in self.rocket.modules if m is not None and m.type == "Tec"),

            total_mass=self.rocket.total_mass
        )

    def handle_two_stage_placement(self, exp_code: str):
        """
        Interaction Stage 2: Handles the players choice of the payload slot.
        Prompts for precise slot destination on the (max-slots + buffer) grid.
        """
        catalog_entry = self.catalog[exp_code]
        module_type, module_name, module_desc, raw_mass = catalog_entry
        module_mass = float(raw_mass)

        while True:
            slot_input = self.view.prompt_for_slot(self.rocket.total_assembly_capacity)

            # Fetches wrong decimal sign input during workbench placement operations
            if "," in slot_input or "." in slot_input:
                self.view.render_slot_input_error()
                continue

            try:
                requested_slot = int(slot_input)

                if 1 <= requested_slot <= self.rocket.total_assembly_capacity:
                    # Unique ID prefix constructor generation via model domain tracking state
                    unique_id = self.rocket.generate_next_instance_id(module_type)

                    new_module = Module(
                        key=exp_code,
                        module_type=module_type,
                        name=module_name,
                        description=module_desc,
                        mass=module_mass
                    )
                    new_module.instance_id = unique_id

                    success = self.rocket.add_module_to_slot(new_module, requested_slot)
                    if success:
                        self.view.render_slot_success(module_name, requested_slot)
                    else:
                        # Maximum flight-ready experiment modules hardware constraint violation
                        self.view.render_slot_limit_error()
                    break

                else:
                    self.view.render_slot_boundary_error(self.rocket.total_assembly_capacity)

            except ValueError:
                self.view.render_slot_input_error()

    def handle_finalization_safeguard(self):
        """
        Catch Engine Guard Framework with try-except context.
        """

        try:
            self.rocket.finalize_and_close_gaps()
            self.view.render_finalization_success(self.rocket.active_instance_ids)

        except ValueError as error:
            # The application intercepted an assembly validation error.
            # Prompt operator for structural recovery option branches (Manual edit / Start over = reset / Exit game).
            while True:
                choice = self.view.render_error_recovery_menu(str(error))

                if choice == "1":
                    break

                elif choice == "2":
                    self.rocket = Rocket()
                    break
                #Exit
                elif choice == "3":
                    self.view.clear_screen()
                    sys.exit(0)

    def run_despin_phase(self) -> float:
        """
        Calculates the despin mass in total and finally divides it in two separate masses.
        Runs validation quiz loops against chosen payload structural parameters.
        """
        self.view.render_phase_two_briefing()

        # ==== SHOW CALCULATION BASE AS ROCKET CONFIGURATION REPORT ====
        # Pull calculated system-wide totals from the model facade layer.
        # Inertia values are in kg*m^2, mass values are in kg.

        i_total = self.rocket.total_inertia
        i_base = ROCKET_BASE_INERTIA
        i_experiments = i_total - i_base

        self.view.render_rocket_configuration_report(i_base, i_experiments, i_total)

        # initialise raw_despin_mass = 0.0
        raw_despin_mass = 0.0

        """
        Player Input: length restricted via core math validation inside physics sublayer.
        The try-except block below serves a dual structural validation purpose:
        # 1. Mathematical: Catches standard parsing failures if string inputs cannot convert to float.
        # 2. Physical: Catches manual ValueErrors raised by the physics engine if constraints are breached.
        
        """
        while True:
            user_input = self.view.prompt_for_despin_length()

            if "," in user_input:
                # Fetches wrong decimal sign input
                self.view.render_despin_input_error()
                continue


            try:

                length_despin = float(user_input)

                # The assignment to 'raw_despin_mass' is strictly required as the baseline
                # payload variable to generate the dynamic correct/incorrect shuffled choices
                # for the interactive Yo-Yo engineering validation quiz directly.
                # calculate_despin_mass: Core math executed under NASA Technical Note D-3848 parameters

                raw_despin_mass = calculate_despin_mass(i_total, length_despin)
                break
            except ValueError as physical_error:
                self.view.render_despin_physics_error(str(physical_error))


        # =====================================================================
        # DE-SPIN Quiz: Calculates mass for a chosen length for YoYo-Deployment
        # =====================================================================

        # Shuffles the correct answers between nearly correct answers to verify player calculations
        despin_mass = float(raw_despin_mass)
        quiz_options = [
            despin_mass,
            round(despin_mass + 0.25, 2),
            round(despin_mass - 0.10, 2)
        ]
        random.shuffle(quiz_options)

        # Run quiz with given answers from listed option arrays
        while True:
            quiz_input = self.view.prompt_for_despin_quiz_answer(quiz_options)

            if "," in quiz_input:
                self.view.render_despin_input_error()
                continue
            try:
                choice = float(quiz_input)
                if choice in quiz_options and choice == despin_mass:
                    break
                else:
                    self.view.render_despin_wrong_answer_warning()
            except ValueError:
                self.view.render_despin_numeric_error()

        # ==== PLAYER FEEDBACK - REVIEW PHASE 2 MOVE TO PHASE 3 LAUNCH PREP
        self.view.render_phase_two_success(despin_mass)
        return despin_mass

    def run_weather_phase(self) -> float:
        """Connects to live satellite APIs and screens conditions for launch safety validation."""
        self.view.clear_screen()
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S LOC")

        # Telemetry Synchronization: Queries remote Open-Meteo REST API using structured parameters
        weather_json = fetch_weather_data(lat=LAUNCH_SITE_LAT, lon=LAUNCH_SITE_LON)
        wind_speed = extract_wind_speed(weather_json)

        self.view.render_weather_telemetry(wind_speed, current_timestamp)

        # Environmental Launch Constraints: Safety threshold audit check
        if wind_speed > MAX_ALLOWABLE_WIND_SPEED:
            self.view.render_launch_scrub()
            sys.exit(1)
        else:
            self.view.render_launch_initialization()
            time.sleep(3)

        self.view.render_weather_nominal_window()
        return wind_speed

    def run_launch_phase(self):
        """Orchestrates flight timeline operational logs and terminal status indicators."""
        self.view.render_launch_operations_log()

        # ===== CALL LAUNCH STATUS BAR ANIMATION LOOPS =====
        self.view.render_flight_status_bars()
        self.view.render_launch_success_interstitial()

    def run_archive_phase(self, wind_speed: float):
        """
        Serializes current campaign tracking snapshots into structured JSON audit records.
        FAIR RDM persistent data storage script processing via specialized service module.
        All physical data get pulled from rocket_object
        """

        saved_file = archive_service.archive_mission(
            rocket_object=self.rocket,
            wind_speed=wind_speed,
            success=True
        )

        # Construct the telemetry text layout report block for the final dashboard
        self.view.render_final_mission_report(
            wind_speed=wind_speed,
            mass_rocket=self.rocket.total_mass,
            i_total=self.rocket.total_inertia,
            chosen_experiments=self.rocket.active_instance_ids,
            saved_file=saved_file
        )
