# views/terminal_view.py
import time
from datetime import datetime
from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.columns import Columns

# Architectural configuration imports
from config.constants import (
    LAUNCH_SITE_NAME,
    LAUNCH_SITE_LAT,
    LAUNCH_SITE_LON,
    MAX_PAYLOAD_SLOTS,
    SPEED_VIZ
)

class TerminalView:
    """
    Handles all visual representation and user interaction rendering for the simulation.
    Ensures the strict separation of console printing logic from core execution controllers.
    """

    def __init__(self):
        self.console = Console()
        self.terminal_width = 80
        # Tracks state shifts for the manual user interface error warning mechanics

    @staticmethod
    def clear_screen():
        """Clears the terminal window using standard operational system hooks."""
        import os
        import subprocess
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True)

    @staticmethod
    def press_enter_to_continue(text: str = "PROCEED"):
        """Blocks execution until the user presses the ENTER key."""
        msg = f"\n[bold blink green]▲ PRESS ENTER TO {text}...[/bold blink green]"
        Prompt.ask(msg)

    #   ===========================================
    #   START WELCOME SCREEN
    #   ===========================================

    def render_welcome_screen(self):
        """Renders the initial startup screen with the blue MAPHEUS banner."""
        self.clear_screen()

        # Render the large ASCII typography banner using pyfiglet
        f = Figlet(font="blocky", width=280)
        mapeus_banner = f.renderText("MAPEUS")

        blue_banner = Panel(
            mapeus_banner,
            style="bold white on blue",
            border_style="blue",
            expand=True
        )
        self.console.print(blue_banner)

        self.console.print("\n" + "=" * self.terminal_width)
        self.console.print("[bold cyan] Welcome to the Sounding Rocket Simulator![/bold cyan]")
        self.console.print("[bold cyan] inspired by the MORABA MAPHEUS Mission - Germany")
        self.console.print("[bold cyan] www.moraba.de/en")
        self.console.print("=" * self.terminal_width + "\n")

        # Pulse/Contrast Warning indicator for PyCharm environments
        self.console.print(
            "[bold blue on white] STATUS: GROUND SYSTEM STANDBY ... AWAITING COMMAND [/bold blue on white]\n")
        self.console.print(" Would you like to assemble your Rocket for your Science Mission?\n\n")

    #   ===========================================
    #   START DISPLAY AND BRIEFING
    #   ===========================================

    @staticmethod
    def prompt_for_start() -> str:
        """Prompts the operator for the critical campaign bootstrap trigger command."""
        return Prompt.ask("Type START to begin the campaign or ESC to exit: ").upper().strip()

    def render_mission_briefing(self):
        """Displays the campaign-wide master operational constraints and phase roadmap."""
        self.clear_screen()

        briefing_text = (
            "[bold yellow]As Mission Manager, your primary task is to clear all PHASES.[/bold yellow]\n\n"
            "To achieve a VALID MISSION status, master this tasks:\n\n"
            "PHASE 1. [bold cyan]PAYLOAD: Preparation of the the Scientific Modules[/bold cyan]\n"
            "         [bold cyan]Total payload volume is limited to[/bold cyan] [bold yellow]10 hardware slots[/bold yellow].\n\n"
            "PHASE 2. [bold cyan]DE-SPIN: Calculate to provide Microgravity[/bold cyan]\n\n"
            "PHASE 3. [bold cyan]LAUNCH-PREP: Check LIVE-Weather Conditions [/bold cyan] \n\n"
            "PHASE 4. [bold cyan]LAUNCH [/bold cyan] \n\n"
            "PHASE 5. [bold cyan]RECOVERY and DATA COLLECTION [/bold cyan]\n"
        )

        mission_panel = Panel(
            briefing_text,
            title="[bold red] MISSION BRIEFING: [/bold red]",
            border_style="cyan",
            expand=True
        )
        self.console.print(mission_panel)
        self.press_enter_to_continue("PROCEED TO CHAPTER 1")

    #   ===========================================
    #   BENCH INTERFACE and MODUL-OPEATION-MESSAGES
    #   ===========================================

    def render_workbench_interface(self, rocket_modules: list, catalog: dict):
        """
        Renders the comprehensive Phase 1 dual-panel workbench layout.
        Splits output into active stack architecture and available warehouse modules.
        """
        self.clear_screen()

        briefing_text_phase_one = (
            "[yellow] Welcome, as Mission Manager, your primary task is to clear the phases.\n\n"
            "[bold white] PHASE 1 PAYLOAD: Assemble the Scientific Modules[/bold white]\n"
            " [bold white]Total payload volume is limited to 10 hardware slots.[/bold white]\n"
        )

        mission_panel = Panel(
            briefing_text_phase_one,
            title="[bold red] EXPERIMENTS MODULES [/bold red]",
            border_style="cyan",
            expand=True
        )
        self.console.print(mission_panel)
        self.console.print()

        # Left Side Layout Matrix: Current configuration state on the active hardware bench
        stack_lines = []
        occupied_count = sum(1 for m in rocket_modules if m is not None)

        if occupied_count == 0:
            stack_lines.append(" Empty BENCH - No Experiments loaded yet")
        else:
            for idx, module in enumerate(rocket_modules):
                slot_number = idx + 1
                if module is None:
                    stack_lines.append(f" Slot {slot_number:02d}: [ EMPTY SLOT ZONE ]")
                else:
                    color = "green" if module.type == "Bio" else "orange3"
                    stack_lines.append(
                        f" Slot {slot_number:02d}: [{color}]{module.instance_id} - {module.name} ({module.mass} kg)[/{color}]")

        stack_lines.append(f" ============ ")
        stack_lines.append(f"Total Modules: {occupied_count} of {MAX_PAYLOAD_SLOTS} (MAX)")

        bench_panel = Panel(
            "\n".join(stack_lines),
            title="[bold cyan]CURRENT PAYLOAD STACK ON BENCH[/bold cyan]\n",
            border_style="cyan",
            expand=False
        )

        # Right Side Layout Matrix: Available inventory serialized straight out of the data catalog
        avail_lines = []
        for key, (typ, name, desc, mass) in catalog.items():
            color = "green" if typ == "Bio" else "orange3"
            avail_lines.append(
                f"\n [bold white]  [{key.upper()}][/bold white] -> [{color}]{name}[/{color}] ({typ} | {mass}kg) - {desc}")

        avail_lines.append("")
        avail_lines.append("[bold white]CONTROLS:[/bold white]")
        avail_lines.append("[bold red][REMOVE ID] -> Remove specific module from slot configuration[/bold red]")
        avail_lines.append("[bold cyan][NEXT]      -> Go to Next TASK: DE-SPIN-System [/bold cyan]")

        available_panel = Panel(
            "\n".join(avail_lines),
            title="[bold cyan]AVAILABLE EXPERIMENTS & CONTROLS[/bold cyan]",
            border_style="cyan",
            expand=False
        )

        self.console.print(Columns([bench_panel, available_panel], equal=True))

    def prompt_workbench_action(self) -> str:
        """Prompts the operator for configuration actions inside the assembly bay."""
        self.console.print(
            "\n [bold white]Enter an [EXP-Code] to ADD, or Enter 'REMOVE [ID]', Finish with 'NEXT': ",
            end="")
        return Prompt.ask().strip().lower()

    @staticmethod
    def ask_slot(cap) -> str:
        return Prompt.ask(f"-> Choose target slot (1-{cap}): ").strip()

    @staticmethod
    def prompt_for_slot(total_capacity: int) -> str:
        """Prompts the engineer for a specific structural workbench target slot."""
        slot_prompt = f"-> Choose target workbench slot (1 to {total_capacity}): "
        return Prompt.ask(slot_prompt).strip()

    def render_slot_success(self, module_name: str, slot: int):
        """Displays a confirmation when a hardware module is successfully mounted."""
        self.console.print(f"\n[OK] Added: {module_name} directly onto Slot {slot}!")
        time.sleep(1)

    def render_slot_limit_error(self):
        """Displays a warning when the physical deployment stack hits hardware maximum limits."""
        self.console.print(f"\n[LIMIT] Stack is full! Maximum {MAX_PAYLOAD_SLOTS} experiment modules allowed.")
        time.sleep(1)

    def render_slot_boundary_error(self, total_capacity: int):
        """Displays an error when the entered slot index falls outside bounds."""
        self.console.print(f"[ERROR] Slot index outside structural boundaries (1-{total_capacity}).")

    def render_slot_input_error(self):
        """Displays a warning on non-integer or malformed decimal slot inputs."""
        self.console.print("[INPUT ERROR] Please enter a valid decimal integer for the target slot.")

    def render_module_removal_success(self, instance_id: str):
        """Confirms successful unmounting of a specific experiment tracking ID."""
        self.console.print(f"\n[OK] Removed experiment module: {instance_id}")
        time.sleep(1)

    def render_module_removal_warning(self, instance_id: str):
        """Warns the user if a removal command targeted a non-existent or empty slot."""
        self.console.print(f"\n[WARN] Nothing to remove. No active module found with ID: '{instance_id}'")
        time.sleep(1)

    def render_generic_command_error(self):
        """Displays a fallback warning for unrecognized or invalid syntax entries."""
        self.console.print("\n[ERROR] Invalid Exp-Code or Command! Please try again.")
        time.sleep(1.5)

    def render_phase_one_complete(self, n_bio: int, mass_bio: float, n_tec: int, mass_tec: float,
                                  total_mass: float):
        """Displays the phase completion matrix and payload engineering structural report."""
        self.console.print()
        self.console.print()

        status_payload = (
            "\n[bold white] STATUS: PHASE 1 COMPLETE - All Experiments are deployed [/bold white]\n\n"
            f" Experiments:"
            f" {n_bio} BIO-MODULES | {mass_bio} kg "
            f" {n_tec} TECHNOLOGY-MODULES | {mass_tec} kg\n"
            f"[bold cyan] TOTAL WEIGHT ROCKET : {total_mass} kg[/bold cyan]\n"
        )

        panel = Panel(status_payload, title="[bold green]STATUS PHASE 1: [/bold green]", border_style="green")
        self.console.print(panel)
        Prompt.ask("[bold blink cyan]▲ PRESS ENTER TO PROCEED ... Calculate the DE-SPIN System[/bold blink cyan]\n")

    def render_finalization_success(self, active_instance_ids: list):
        """Displays final structural confirmation when the payload deck locks for flight."""
        self.console.print("\n[STATUS] PHASE 1 COMPLETE - All Experiments are deployed and locked.")
        self.console.print(f" Active Experiment Modules | IDs -> flight-ready : {active_instance_ids}")
        time.sleep(2)

    #   ===========================================
    #   DE-SPIN SYSTEM DIALOGS
    #   ===========================================

    def render_phase_two_briefing(self):
        """Briefs the player on NASA Yo-Yo De-Spin mechanics and scientific microgravity prerequisites."""
        self.clear_screen()

        briefing_text = (
            " [bold yellow]PHASE 2: \n ENGINEERING TASK: Calculate DE-SPIN SYSTEM to provide Microgravity[/bold yellow]\n\n"
            "To deploy experiments safely, the rocket 4 Hz rotation must be reduced to ~ 0 Hz.\n"
            "We achieve this by deploying [bold red]two mechanical counterweights on extendable deployment wires.[/bold red]\n\n"
            "Its called the Yo-Yo-Despin System\n\n"
            "[bold cyan]THE PHYSICAL FORMULA (NASA Technical Note D-3848):[/bold cyan]\n\n"
            " We need the mass induced Inertia of the Full-Payload to calculate the Counterweight Mass.\n\n"
            " 1. [bold green]Sum up the Moments of Inertia: MAPEUS System I + Scientific Modules I[/bold green]\n\n"
            " 2. [bold yellow]Choose the LENGTH of the WIRES[/bold yellow]\n\n"
            " 3. [bold yellow]Calculate (Approximate) the DE-SPIN Mass[/bold yellow]\n"
        )

        mission_panel = Panel(briefing_text, title="PHASE 2: DE-SPIN CALCULATION", border_style="cyan", expand=True)
        self.console.print(mission_panel)
        self.console.print()
        Prompt.ask(
            "[bold blink green]\n START Calculation for  DE-SPIN  ▲ PRESS ENTER TO PROCEED ...[/bold blink green]\n")

    def render_rocket_configuration_report(self, i_base: float, i_experiments: float, i_total: float):
        """Displays real-time inertia values calculated across the integrated structural components."""
        config_summary = (
            f" \n {i_base:.2f} kg*m^2   --> Basic-MAPEUS-Moment of inertia\n"
            f" {i_experiments:.2f} kg*m^2   --> Summarized Moment of inertia all Experiments \n\n"
            f" ==========================\n"
            f" [bold green]{i_total:.2f} kg*m^2   --> Summarized Moment of inertia the rocket: I total [/bold green]\n\n"
            f" Calculate the DE-SPIN Mass \n"
            f" [bold red]m = I / (L^2)[/bold red]\n"
        )

        result_panel = Panel(config_summary, title="[bold yellow] * ROCKET CONFIGURATION REPORT * [/bold yellow]",
                             border_style="green", expand=True)
        self.console.print(result_panel)
        self.console.print()

    @staticmethod
    def prompt_for_despin_length() -> str:
        """Prompts the user to enter the designated Yo-Yo deployment wire length."""
        return Prompt.ask("Choose the length of the DE-SPIN wire -> L in [m]: ").strip()

    def prompt_for_despin_quiz_answer(self, quiz_options: list) -> str:
        """Displays the approximation options and prompts the user for the quiz answer."""
        self.console.print(f"[bold yellow]APPROXIMATE the MASS per YO-YO [kg] [/bold yellow] \n")
        self.console.print(f"\n[bold red]{[f'{num:.2f}' for num in quiz_options]}[/bold red]\n")
        return Prompt.ask("Enter the correct weight from the listed options: ").strip()

    def render_despin_input_error(self):
        """Warns the user about improper comma separation instead of a decimal dot."""
        self.console.print("\n[INPUT ERROR] Use a decimal dot (.) instead of a comma (,).\n")

    def render_despin_physics_error(self, error_message: str):
        """Displays engineering violations when wire lengths breach predefined constraints."""
        self.console.print(f"\n[PHYSICS ERROR] {error_message}")
        Prompt.ask("Press any key to continue...")

    def render_despin_wrong_answer_warning(self):
        """Displays feedback when quiz answers do not match the physical equations."""
        self.console.print(f"\n(CALCULATION WRONG - Try AGAIN!)\n")

    def render_despin_numeric_error(self):
        """Demands a clean valid decimal format if input parsing crashes."""
        self.console.print("\nPlease enter a valid decimal number.\n")

    def render_phase_two_success(self, despin_mass: float):
        """Renders the validation confirmation panel once the De-Spin equations match telemetry."""
        status_payload = (
            " [bold green]* STATUS: SUCCESS - > DE-SPIN CALCULATION COMPLETED[bold green]\n"
            f"[bold white]* DE-SPIN Weights deployed : {despin_mass} kg\n"
            " * PHASE 1 COMPLETE --> \n"
            " * PHASE 2 COMPLETE --> [/bold white]\n"
            "[bold cyan] * READY For PHASE 3 -> LAUNCH PREPARATION[/bold cyan]\n"
        )
        panel = Panel(status_payload, title="[bold green]STATUS PHASE 3: [/bold green]", border_style="green")
        self.console.print(panel)
        Prompt.ask("[bold blink green] ▲ PRESS ENTER TO PROCEED ... TO PHASE 4: LAUNCH [/bold blink green]\n")

    #   ===========================================
    #   WEATHER, FLIGHT ANIMATION and FINAL REPORT
    #   ===========================================

    def render_weather_telemetry(self, wind_speed: float, current_timestamp: str):
        """Prints the real-time atmospheric telemetry sync block for the targeted launch pad."""
        telemetry_log = (
            f"* [bold white]Launch Site Coordinates:[/bold white]   "
            f"Lat {LAUNCH_SITE_LAT}, Lon {LAUNCH_SITE_LON} ({LAUNCH_SITE_NAME})\n"
            f"* [bold white]API Connection Status:[/bold white] [bold green]    ONLINE (HTTP 200 OK)[/bold green]\n"
            f"* [bold white]Telemetry Synchronization:[/bold white] [bold cyan]  {current_timestamp}[/bold cyan] "
            f"[dim](Real-Time Live Feed)[/dim]\n\n"
            f"* [bold white]Registered Wind Speed: [Live-Feed][/bold white] "
            f"[bold green]    {wind_speed} km/h [/bold green][dim](Real-Time Live Feed)[/dim]"
        )

        self.console.print(Panel(
            telemetry_log,
            title="[bold yellow] LIVE PAD - TELEMETRY[/bold yellow]",
            border_style="yellow",
            expand=False,
            padding=(2, 2),
        ))
        self.console.print("\n")

    def render_launch_scrub(self):
        """Prints a hard critical safety warning when local flight parameter windows close."""
        self.console.print(
            "[bold red]LAUNCH SCRUBBED: Extreme wind conditions detected! Safety limits exceeded.[/bold red]")

    def render_launch_initialization(self):
        """Displays status messages while the launch system matches rail alignment targets."""
        self.console.print("[bold yellow] STATUS ADJUSTING LAUNCHER ...[/bold yellow]")

    @staticmethod
    def render_weather_nominal_window():
        """Confirms local launch clearance parameters are structurally certified for liftoff."""
        Prompt.ask(
            "\n [bold green]Weather window is nominal. Launcher in Position. [/bold green]  ▲ PRESS ENTER TO PROCEED ...")

    def render_launch_operations_log(self):
        """Prints the master operational flight log block prior to initiating countdown."""
        launch_log = " LAUNCH & DISPLAY of FLIGHT OPERATIONS "
        self.console.print(Panel(
            launch_log,
            title="[bold gold1] LOG [/bold gold1]",
            border_style="red",
            expand=False,
            padding=(1, 2),
        ))

    @staticmethod
    def render_flight_status_bars(length: int = 60):
        """Animates real-time ascent and descent flight tracking status metrics via stdout."""
        for i in range(length + 1):
            percent = int((i / length) * 100)
            bar = "█" * i + "░" * (length - i)

            if percent < 10:
                status_text = "Launch -> High-thrust propulsion burning...  "
                delay = 0.02 * SPEED_VIZ
            elif percent < 25:
                status_text = "Burnout & rocket motors separated!          "
                delay = 0.15 * SPEED_VIZ
            elif percent < 30:
                status_text = "DE-SPIN successful - Rotation 0 Hz          "
                delay = 0.15 * SPEED_VIZ
            else:
                status_text = "Microgravity phase active                   "
                delay = 0.12 * SPEED_VIZ

            print(f"\rStatus UP   | {status_text} | [{bar}] {percent:3}%", end="", flush=True)
            time.sleep(delay)

        time.sleep(0.5)
        print()

        for i in range(length, -1, -1):
            percent = int((i / length) * 100)
            bar = "█" * i + "░" * (length - i)

            if percent > 30:
                status_text = "STATUS: Microgravity experiments running... "
                delay = 0.12 * SPEED_VIZ
            elif percent == 0:
                status_text = "Landed - Helicopter for Recovery deployed!  "
                delay = 0.35 * SPEED_VIZ
            else:
                status_text = "Recovery-System deployed -> Parachute open  "
                delay = 0.35 * SPEED_VIZ

            print(f"\rStatus DOWN | {status_text} | [{bar}] {percent:3}%", end="", flush=True)
            time.sleep(delay)

        print()

    def render_launch_success_interstitial(self):
        """Renders flight validation transition delays to prepare final data serialization reports."""
        self.console.print()
        self.console.print("\n PHASE 4: LAUNCH - > SUCCESSFUL COMPLETED ... ")
        self.console.print()
        self.console.print(" [bold green] ======= PREPARING MISSION REPORT=============[/bold green]\n")
        self.console.print()
        time.sleep(2)

    def render_final_mission_report(self, wind_speed: float, mass_rocket: float, i_total: float,
                                    chosen_experiments: list, saved_file: str):
        """Displays the comprehensive FAIR-compliant operational report overview board."""
        report_text = (
            f"[bold white]TITLE:[/bold white]          Mission Report - Mission Manager Task: MAPEUS \n"
            f"[bold white]TIMESTAMP:[/bold white]      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"[bold white]LAUNCH SITE:[/bold white]    {LAUNCH_SITE_NAME} (Lat {LAUNCH_SITE_LAT}, Lon {LAUNCH_SITE_LON})\n"
            f"----------------------------------------------------------------------\n"
            f"[bold white]WIND VELOCITY:[/bold white]  [bold green]{wind_speed} km/h[/bold green] (Nominal Window)\n"
            f"[bold white]ROCKET MASS:[/bold white]    [bold cyan]{mass_rocket} kg[/bold cyan]\n"
            f"[bold white]TOTAL INERTIA:[/bold white]  [bold cyan]{i_total:.2f} kg*m^2[/bold cyan]\n"
            f"----------------------------------------------------------------------\n"
            f"[bold white]PAYLOAD COUNT:[/bold white]  {len(chosen_experiments)} Modules deployed\n"
            f"[bold white]EXPERIMENTS:[/bold white]    [bold green]{chosen_experiments}[/bold green]\n\n"
            f"----------------------------------------------------------------------\n"
            f"[bold white]DATA ARCHIVE:[/bold white]   [dim]{saved_file}[/dim]\n"
        )

        mission_report_panel = Panel(
            report_text,
            title="[bold gold1] FINAL MISSION REPORT and DATA ARCHIVE [/bold gold1]",
            border_style="gold1",
            expand=False,
            padding=(1, 2)
        )

        self.console.print()
        self.console.print(mission_report_panel)
        self.console.print("\n" + "=" * self.terminal_width)
        self.console.print(
            "[bold gold1] ** MISSION SUCCESSFUL! ** Ground control logging out. Goodbye![/bold gold1]")
        self.console.print("=" * self.terminal_width + "\n")
        Prompt.ask("Press ENTER to close the ground system console...")

    def render_error_recovery_menu(self, error_message: str) -> str:
        """Renders the comprehensive blueprint structural validation error bypass panel."""
        self.console.print("\n" + "!" * 70)
        self.console.print(f"[ALERT] STRUCTURAL BOUNDARY SAFETY ENGINE GUARD TRIGGERED:")
        self.console.print(f"-> {error_message}")
        self.console.print("!" * 70)
        self.console.print("The application intercepted an assembly error. Choose a recovery option:")
        self.console.print(" Option: Return straight to the workbench editing grid to manually modify layout.")
        self.console.print(" Option: Clear the entire active workbench layout to reset blueprint from scratch.")
        self.console.print(
            " Option: Terminate deployment operations and safely abort ground console control systems.")

        return Prompt.ask("\nEnter recovery option", choices=["1", "2", "3"]).strip()
