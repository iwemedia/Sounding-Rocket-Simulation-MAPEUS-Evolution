# ==============================
#          CS50 Informations
# ==============================
"""
your project’s title: The SOUNDING-ROCKET Mission Manager Simulator

your name: Iris
your GitHub and edX usernames:  iveive
your city and country: Berlin, Germany
and, the date you have recorded this video: 13. Oktober 2016

"""
# ==============================
#         IMPORTS
# ==============================

import os
import sys
import subprocess
import requests
import random
import json
import time

from pyfiglet import Figlet
from rich.columns import Columns
from rich.console import Console
from datetime import datetime
from rich.panel import Panel


# ===========================
#  CONSTANTS
# ===========================

# Wire length limits for Yo-Yo De-Spin System (in meters) - PHASE 2
MIN_WIRE_LENGTH = 0.80
MAX_WIRE_LENGTH = 3.00

# Definition of fallback if API Request is failing -> PHASE 3
DEFAULT_WIND_SPEED = 12.5

# Esrange Launch Site Configuration -> PHASE 3
LAUNCH_SITE_NAME = "Esrange, Sweden"
LAUNCH_SITE_LAT = 67.892
LAUNCH_SITE_LON = 21.106

#speed factor for visualisiation rocket launch -> PHASE 4
SPEED_VIZ = 2

# ==============================
#  Instantiation for console & terminal
# ==============================

console = Console()
terminal_w = 80

# ===============================
#         MAIN CODE BLOCK
# ===============================

def main():

    clear_screen()

    # -------- START-SCREEN

    f = Figlet(font="blocky", width=280)
    mapeus_banner = f.renderText("MAPEUS")

    blue_banner: object = Panel(
        mapeus_banner,
        style="bold white on blue",
        border_style="blue",
        expand=True
    )

    console.print(blue_banner)

    console.print("\n" + "=" * terminal_w)
    console.print("[bold cyan] Welcome to the Sounding Rocket Simulator![/bold cyan]")
    console.print("[bold cyan] inspired by the MORABA MAPHEUS Mission - Germany")
    console.print("[bold cyan] www.moraba.de/en")
    console.print("=" * terminal_w + "\n")

    # Pulse/Contrast Warning indicator for PyCharm
    console.print("[bold blue on white] STATUS: GROUND SYSTEM STANDBY ... AWAITING COMMAND [/bold blue on white]\n")
    console.print(" Would you like to assemble your Rocket for your Science Mission?\n\n")

    # Track state shifts for the manual user interface error warning
    error_pulse = False


    # ---- ASK FOR USER INPUT TO START ----

    while True:
        choice = input("Type START to begin the campaign or ESC to exit: ").upper().strip()

        if choice == "ESC":
            console.print("\n" + "=" * terminal_w)
            console.print("Mission aborted. Ground control logging out. Goodbye!")
            console.print("=" * terminal_w + "\n")
            sys.exit(0)

        elif choice == "START":
            break

        else:
            clear_screen()
            console.print(blue_banner)
            console.print("\n" + "=" * terminal_w)
            console.print("[bold cyan]Welcome to the Sounding Rocket Simulator![/bold cyan]")
            console.print("=" * terminal_w + "\n")

            # Pulse color swap mechanics on user input typing errors
            if not error_pulse:
                console.print("[bold white on red] ALERT: INVALID COMMAND DETECTED ... RE-ENTER [/bold white on red]\n")
                error_pulse = True
            else:
                console.print("[bold black on red] ALERT: INVALID COMMAND DETECTED ... RE-ENTER [/bold black on red]\n")
                error_pulse = False

            console.print("[bold red]Command not recognized. Please type START or ESC.[/bold red]\n")

    #   --- THE CAMPAIGN BEGINS ---
    clear_screen()

    # Welcome and MISSION BRIEFING
    briefing_text_mission = (

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
        briefing_text_mission,
        title="[bold red] MISSION BRIEFING: [/bold red]",
        border_style="cyan",
        expand=True
    )
    # Print Mission Panel -> Wait
    console.print(mission_panel)
    console.print("\n[bold blink green]▲ PRESS ENTER TO PROCEED TO CHAPTER 1 (PAYLOAD MODULE SPECS)...[/bold blink green]")
    input()

    # ------- PHASE 1 - CHAPTER 1: PAYLOAD MODULE SPECS

    # Dictionary for Experiments
    # format: "key": (typ, name, description, mass in kg)
    EXPERIMENTE = {
        "roms": ("Bio", "ROMS", "Human Stem Cells", 14.5),
        "gen2": ("Bio", "GEN-2", "Insect Behavioral Research", 14.5),
        "aquafish": ("Bio", "AQUAFISH", "Fish Motion Sickness Lab", 14.5),
        "cosmo": ("Tec", "COSMO", "Flight Computer & Heat Shield", 29),
        "resitek": ("Tec", "RESITEK", "Space Weather GNSS", 29),
        "watches": ("Tec", "WATCHES", "Watches in Microgravity", 29)
    }

    # ==== BACKGROUND CALCULATIONS

    #Call function for payload assembling -> task 1
    n_bio, n_tec,chosen_experiments = start_payload_stack(EXPERIMENTE)

    # Calculate Configuration Variables of Mass and Inhertia - task 2
    (i_base, i_experiments, i_total, mass_bio_total, mass_tec_total, mass_rocket) = calculate_rocket_configuration(n_bio, n_tec)


    # ==== PLAYER FEEDBACK - REVIEW PHASE 1 MOVE TO PHASE 2

    #  Print Mission Panel -> Wait
    console.print()
    console.print()

    status_payload = (
        "\n[bold white] STATUS: PHASE 1 COMPLETE - All Experiments are deployed [/bold white]\n\n"
        f" Experiments:"
        f" {n_bio} BIO-MODULES | {mass_bio_total} kg "
        f" {n_tec} TECHNOLOGY-MODULES | {mass_tec_total} kg\n"
        f"[bold cyan] TOTAl WEIGHT ROCKET : {mass_rocket} [/bold cyan]\n"
    )

    panel = Panel(
        status_payload,
        title="[bold green]STATUS PHASE 1: [/bold green]",
        border_style="green",

    )

    console.print(panel)
    console.print("[bold blink cyan]▲ PRESS ENTER TO PROCEED ... Calculate the DE-SPIN System[/bold blink cyan]\n")
    input()

    # ==== PHASE 2: DE-SPIN SYSTEM CALCULATION

    clear_screen()

    # Player Briefing De-SPIN Calculation

    briefing_text_phase_two = (
        " [bold yellow]PHASE 2: \n ENGINEERING TASK: Calculate DE-SPIN SYSTEM to provide Microgravity[/bold yellow]\n\n"
        "To deploy experiments safely, the rocket 4 Hz rotation must be reduced to ~ 0 Hz.\n"
        "We achieve this by deploying [bold red]two mechanical counterweights on extendable deployment wires.[/bold red]\n\n"
        "Its called the Yo-Yo-Despin System\n"
        
        "[bold cyan]THE PHYSICAL FORMULA (NASA Technical Note D-3848):[/bold cyan]\n\n"
        " We need the mass induced Inhertia of the Full-Payload to calculate the Counterweight Mass.\n\n"

       
        " 1. [bold green]Sum up the Moments of Inertia: MAPEUS System I + Scientific Modules I[/bold green]\n\n"
        " 2. [bold yellow]Choose the LENGTH of the WIRES[/bold yellow]\n\n"
        " 3. [bold yellow]Calculate (Approximate) the DE-SPIN Mass[/bold yellow]\n\n"
    )

    mission_panel_phase_two = Panel(
        briefing_text_phase_two,
        title="PHASE 2: DE-SPIN CALCULATION",
        border_style="cyan",
        expand=True
    )

    console.print(mission_panel_phase_two)
    console.print()

    console.print("[bold blink green]\n START Calculation for  DE-SPIN  ▲ PRESS ENTER TO PROCEED ...[/bold blink green]\n")
    input()

    # ==== SHOW CALCULATION BASE AS ROCKET CONFIGURATION REPORT ====
    # Inertia values are in kg*m^2, mass values are in kg

    config_summery = (
        f" \n {i_base:.2f} kg*m^2   --> Basic-MAPEUS-Moment of inertia\n" 
        f" {i_experiments:.2f} kg*m^2   --> Summerized Moment of inertia all Experiments \n\n"
        f" ==========================\n"
        f" [bold green]{i_total:.2f} kg*m^2   --> Summerized Moment of inertia the rocket: I total [/bold green]\n\n"
        f" Calculate the DE-SPIN Mass \n"
        f" [bold red]m = I / (L^2)[/bold red]\n"
    )

    result_panel = Panel(
        config_summery,
        title="[bold yellow] * ROCKET CONFIGURATION REPORT * [/bold yellow]",
        border_style="green",
        expand=True
    )

    console.print(result_panel )
    console.print()

    # ==== Quiz: calculate mass for a chosen length for YoYo-Deployment

    raw_despin_mass = run_despin_quiz(i_total)

    #rounding  before quiz to catch
    despin_mass = float(raw_despin_mass)

    # shuffle the correct answers between nearly correct answers
    despin_list_quiz = [
        despin_mass,
        round(despin_mass + 0.25, 2 ),
        round(despin_mass - 0.10, 2),
    ]
    random.shuffle(despin_list_quiz)

    #formated list
    formatted_despin_list_quiz = [f"{num:.2f}" for num in despin_list_quiz]

    console.print (f"[bold yellow]APPROXIMATE the MASS per YO-YO [kg] [/bold yellow] \n")
    console.print( f"\n[bold red]{formatted_despin_list_quiz}[/bold red]\n")

    # Run quiz with given answers
    while True:
        quiz_input = input(f" Enter the correct weight from the listed options: ")

        if "," in quiz_input:
            console.print("\n[bold red] INPUT ERROR: Use a decimal dot (.) instead of a comma (,).[/bold red]\n")
            continue

        try:
            despin_choice = float(quiz_input)

            if despin_choice in despin_list_quiz and despin_choice == despin_mass:
                break

            else:
                console.print(f"\n([bold red] CALCULATION WRONG - Try AGAIN![bold red])\n")

        except ValueError:
            console.print("\n[bold red] Please enter a valid decimal number.[/bold red]\n")

    # ==== PLAYER FEEDBACK - REVIEW PHASE 2 MOVE TO PHASE 3 LAUNCH PREP

    #  Print Mission Panel -> Wait
    status_payload = (
        " [bold green]* STATUS: SUCCESS - > DE-SPIN CALCULATION COMPLETED[bold green]\n"
        f"[bold white]* DE-SPIN Weights deployed : {despin_mass}"
        " * PHASE 1 COMPLETE --> "
        " * PHASE 2 COMPLETE --> [/bold white]"
        "[bold cyan] * READY For PHASE 3 -> LAUNCH PREPARATION[/bold cyan]\n"
    )
    panel = Panel(
        status_payload,
        title="[bold green]STATUS PHASE 3: [/bold green]",
        border_style="green",
    )

    console.print (panel)
    console.print ("[bold blink green] ▲ PRESS ENTER TO PROCEED ... TO PHASE 4: LAUNCH [/bold blink green]\n")
    input()


    clear_screen()

    # ==== PHASE 3: LAUNCH PAD Adjustment -> Weather API for Esrange : lat=67.892, lon=21.106

    # import datetime locally
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S LOC")

    # instanz of Class WeatherService
    weather_json = fetch_weather_data(lat=LAUNCH_SITE_LAT, lon=LAUNCH_SITE_LON)
    wind_speed = extract_wind_speed(weather_json)

    telemetry_log = (
        f"* [bold white]Launch Site Coordinates:[/bold white]   "
        f"Lat {LAUNCH_SITE_LAT}, Lon {LAUNCH_SITE_LON} ({LAUNCH_SITE_NAME})\n"
        f"* [bold white]API Connection Status:[/bold white] [bold green]    ONLINE (HTTP 200 OK)[/bold green]\n"
        f"* [bold white]Telemetry Synchronization:[/bold white] [bold cyan]  {current_timestamp}[/bold cyan] "
        f"[dim](Real-Time Live Feed)[/dim]\n\n"
        f"* [bold white]Registered Wind Speed: [Live-Feed][/bold white] "
        f"[bold green]    {wind_speed} km/h [/bold green][dim](Real-Time Live Feed)[/dim]"
    )

    console.print (Panel(
        telemetry_log,
        title="[bold yellow] LIVE PAD - TELEMETRY[/bold yellow]",
        border_style="yellow",
        expand=False,
        padding=(2,2),
    ))
    console.print("\n")

    if wind_speed > 30.0:
        console.print ("[bold red]LAUNCH SCRUBBED: Extreme wind conditions detected! Safety limits exceeded.[/bold red]")
        sys.exit(1)

    else:
        console.print ("[bold yellow] STATUS ADJUSTING LAUNCHER ...[/bold yellow]" )
        # print_rocket
        time.sleep(3)

    console.print ("\n [bold green]Weather window is nominal. Launcher in Position. [/bold green]  ▲ PRESS ENTER TO PROCEED ...")
    input()

    # ==== PHASE 4: LAUNCH & DISPLAY of FLIGHT OPERATIONS

    launch_log = (
        f" LAUNCH & DISPLAY of FLIGHT OPERATIONS "
    )

    console.print(Panel(
        launch_log,
        title="[bold gold1] LOG [/bold gold1]",
        border_style="red",
        expand=False,
        padding=(1, 2),
    ))


    # ===== CALL LAUNCH STATUS BAR
    launch_status_bar(60)

    console.print()
    console.print ("\n PHASE 4: LAUNCH - > SUCCESSFUL COMPLETED ... ")
    console.print()
    console.print (" [bold green] ======= PREPARING MISSION REPORT=============[/bold green]\n")
    console.print()
    time.sleep(2)

    # ==== PHASE 5: MISSION REPORT and DEBRIEF

    # FAIR RDM data storage script
    saved_file = archive_mission_data(chosen_experiments, EXPERIMENTE, wind_speed)

    # Construct the telemetry text layout for the final overview
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

    # FINAL PANEL

    mission_report_panel = Panel(
        report_text,
        title="[bold gold1] FINAL MISSION REPORT and DATA ARCHIVE [/bold gold1]",
        border_style="gold1",
        expand=False,
        padding=(1, 2)
    )

    console.print()
    console.print(mission_report_panel)
    console.print("\n" + "=" * terminal_w)
    console.print("[bold gold1] ** MISSION SUCCESSFULL! ** Ground control logging out. Goodbye![/bold gold1]")
    console.print ("=" * terminal_w + "\n")

    # final closing
    input("Press ENTER to close the ground system console...")


# =========================
#      FUNCTIONS
# =========================

def clear_screen():
        #clears the terminal window using subprocess module
        command = "cls" if os.name == 'nt' else 'clear'
        subprocess.run(command, shell=True)

def start_payload_stack(experimente):
    # List for Payload Stack
    payload_stack = []

    #Mission Briefing STAGE 1: PAYLOAD
    briefing_text_phase_one = (
        "[yellow] Welcome, as Mission Manager, your primary task is to clear the phases.\n\n"
        "[bold white] PHASE 1 PAYLOAD: Assemble the Scientific Modules[/bold white]\n"
        " [bold white]Total payload volume is limited to 10 hardware slots.[/bold white]\n"
    )

    # TASK ASSEMBLING PAYLOAD
    while True:
        clear_screen()

        # Print Mission Panel -> Wait
        mission_panel = Panel(
            briefing_text_phase_one,
            title="[bold red] EXPERIMENTS MODULES [/bold red]",
            border_style="cyan",
            expand=True
        )
        console.print(mission_panel)
        console.print()

        #Left side panel: CURRENT PAYLOAD STACK ON BENCH

        stack_lines = []

        if not payload_stack:
            stack_lines.append(" Emthy BENCH - No Experiments loaded yet")

        else:
            # prints chosen module
            for i, exp_key in enumerate(reversed(payload_stack)):
                slot_number = len(payload_stack) - i
                exp_type = experimente[exp_key][0]
                exp_name = experimente[exp_key][1]

                #color coded experiments
                color = "green" if exp_type == "Bio" else "orange3"
                stack_lines.append(f"\n Slot: {slot_number:02d}: [{color}]{exp_type}  - [{color}]{exp_name}")

        stack_lines.append(f" ============ ")
        stack_lines.append(f"Total Modules: {len(payload_stack)} of 10 (MAX)")

        bench_panel = Panel(
            "\n".join(stack_lines),
            title="[bold cyan]CURRENT PAYLOAD STACK ON BENCH[/bold cyan]\n",
            border_style="cyan",
            expand=False
        )

        # right side - BENCH PANEL: all available Experiments
        avail_lines = []
        for key, (typ, name, desc, mass) in experimente.items():
            # match colors to stack on bench
            color = "green" if typ == "Bio" else "orange3"
            avail_lines.append(
                f"\n [bold white]  [{key.upper()}][/bold white] -> [{color}]{name}[/{color}] ({typ} | {mass}kg) - {desc}")

        # SHOW CONTROLS TO PLAYER
        avail_lines.append("")
        avail_lines.append("[bold white]CONTROLS:[/bold white]")
        avail_lines.append("[bold red][REMOVE]   -> Remove the top experiment (just below Nose Cone)[/bold red]")
        avail_lines.append("[bold green][START]   -> Confirm payload configuration finished [/bold green]")
        avail_lines.append("[bold cyan][NEXT]   -> Go to Next TASK: DE-SPIN-System [/bold cyan]")

        # SHOW AVAILABLE EXPERIMENTS TO PLAYER

        available_panel = Panel(
            "\n".join(avail_lines),
            title="[bold cyan]AVAILABLE EXPERIMENTS & CONTROLS[/bold cyan]",
            border_style="cyan",
            expand=False
        )

        # SHOW IN TERMINAL - besides if possible
        console.print(Columns([bench_panel, available_panel], equal=True))

        # PLAYER INPUT in rich-styled
        console.print("\n [bold white]Enter an [EXP-Code] to ADD, or Enter 'REMOVE', "
                      "Finish with 'NEXT': ", end="")
        user_input = input().strip().lower()


        # Action: START
        if user_input == "next":
            if not payload_stack:
                console.print("\n [bold red]You cannot launch an empty rocket! Add at least 1 experiment.")
                time.sleep(2)
                continue
            break

        # Action: REMOVE
        elif user_input == "remove":
            if payload_stack:
                removed_item = payload_stack.pop()
                console.print(f"\n Removed experiment: {experimente[removed_item][1]}")
            else:
                console.print("\n Nothing to remove.")
            time.sleep(1)

        # Action: ADD EXPERIMENT
        elif user_input in experimente:
            if len(payload_stack) >= 10:
                console.print("\n Stack is full! Maximum 10 experiments allowed.")
            else:
                payload_stack.append(user_input)
                console.print(f"\n Added: {experimente[user_input][1]}")
            time.sleep(0.3)

        # ERROR HANDLING
        else:
            console.print("\n Invalid Exp-Code! Please try again.")
            time.sleep(1.5)


    # SUM Experiments and RETURN
    n_bio = sum(1 for exp in payload_stack if experimente[exp][0] == "Bio")
    n_tec = sum(1 for exp in payload_stack if experimente[exp][0] == "Tec")

    return n_bio, n_tec, payload_stack


def calculate_rocket_configuration(n_bio: int, n_tec: int) -> tuple[float, float, float, float, float, float]:
    """
    Calculates the total inertia and total masses for the chosen experiments.
    Inertia values are in kg*m^2, mass values are in kg.

    Parameters:
    n_bio (int): Number of biological experiment modules
    n_tec (int): Number of technological experiment modules

    Returns:
    tuple: (i_base, i_experiments, i_total, mass_bio_total, mass_tec_total, mass_rocket)
    """

    # approx fixed base inertia of the rocket system (service + recovery module) d = 365 mm MORPHEUS
    i_base = 1.50

    # Pre-defined game design values for inertia per module for easy player-calculation
    i_per_bio = 0.25
    i_per_tec = 0.50

    # mass [kg] definitions per module type biological or technological payload and base_mass based on MORPHEUS
    mass_per_bio = 14.5
    mass_per_tec = 29.0
    mass_base_mapheus = 85.0

    # Calculate inertia contributions i_base
    i_experiments = (n_bio * i_per_bio) + (n_tec * i_per_tec)
    i_total = i_base + i_experiments

    # Calculate total masses for the player interface
    mass_bio_total = n_bio * mass_per_bio
    mass_tec_total = n_tec * mass_per_tec
    mass_rocket = mass_bio_total + mass_tec_total + mass_base_mapheus

    # Returns all calculated variables -> for flexibility in player interaction
    return i_base, i_experiments, i_total, mass_bio_total, mass_tec_total, mass_rocket


def run_despin_quiz(i_total):
    """
    Calculates the despin mass in total and finally divided it in two separate masses
    from Player Input: length < restricted to >= 0.8 <= 3 meter.
    returns: half despin_mass in [kg]
    """

    while True:
        user_input = input("Choose the length of the DE-SPIN wire -> L in [m]: ")
        console.print()

        if "," in user_input:
            # fetches wrong decimal sign input
            console.print("\n[bold red] INPUT ERROR: Use a decimal dot (.) instead of a comma (,).[/bold red]\n")
            input("Press any key to continue...")
            continue

        try:
            lengths_despin = float(user_input)

            if lengths_despin < MIN_WIRE_LENGTH or lengths_despin > MAX_WIRE_LENGTH:
                console.print(f"\n[bold red] Invalid length option, choose between {MIN_WIRE_LENGTH:.2f} m "
                              f"and {MAX_WIRE_LENGTH:.2f} m. Try again.[/bold red]")
                input("Press any key to continue...")
                continue

            # calculate one of two de-spin masses
            despin_mass = round((i_total / (lengths_despin ** 2))/2, 2)
            return despin_mass

        except (ZeroDivisionError, ValueError):
            console.print(f"\n[bold red] That's not a valid number, choose between 0,8 m and 3.00 m. "
                          f"Try again.[/bold red]")
            input("Press any key to continue...")


def fetch_weather_data(lat, lon):
    """
    Queries the remote Open-Meteo REST API using structured parameters.
    Returns the current surface wind velocity metric at a 10m altitude.

    * Fix 001: problem automated blocking of py-script request - > API -> custom header:
    Based on: [ https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers]
    Based on: [https://www.youtube.com/watch?v=4m0Hncf1aAU]
    ** Fixed that the Open-Meteo REST API rejected connection requests from the
    simulation, causing the script to continuously fall back to the offline `DEFAULT_WIND_SPEED` metric.
    ** by implementing a custom Identity Signatures (Header Spoofing User Agent):
    ** with a structured `headers` dictionary containing a realistic web browser fingerprint,
    into authorizing the automated script as a human client session.

    * Fix 002: clear up the messy URL query by using dictionary Payload Arrays:
    Source: [ Requests Documentation by Kenneth Ritz: https://requests.readthedocs.io/_/downloads/en/v2.9.1/pdf/]
    ** Extracted embedded raw URL queries and migrated them into a clean, separated argument layout
    (`payload = { ... }`). By passing this configuration directly into the `requests.get(url, params=payload)` pipeline,
    the networking engine builds a perfectly formatted, standard-compliant URL string automatically.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    #dictionary URL Fix 002
    payload = {
        "latitude": lat,
        "longitude": lon,
        "current": "wind_speed_10m"
    }

    # declare User-Agent Fix 001
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        # Fixes 001 - 002 - 003
        response = requests.get(url, params=payload, headers=headers, timeout=5)

        if response.status_code == 200:
            return response.json()

    except requests.RequestException:
        # fall back
        pass

    return {}

def extract_wind_speed(weather_data)     -> float:

    """
    Extracts the current surface wind velocity metric at a 10m altitude.
    Returns fallback DEFAULT_WIND_SPEED if validation fails.

    * Fix 003: Secured Silent Except-Triggers (Strict API Contract Validation):
    Based on: [try-except block: https://docs.python.org/3/library/http.client.html]
    ** Handling data payload extraction logic by embedding explicit key-existence audits
    (`if "current" in data ...`) prior to executing structural float type castings.
    This insulates the data validation pipeline from crashing on malformed JSON packages.
    """

    try:
        # Verify key existence before casting
        if "current" in weather_data and "wind_speed_10m" in weather_data["current"]:
            # Directly return the float value
            return float(weather_data["current"]["wind_speed_10m"])

    except (KeyError, ValueError):
        # fallback for pipeline breaks and fall through
        pass

    return DEFAULT_WIND_SPEED

def launch_status_bar(laenge=40):
    # === Phase 1: UP (Ascent to Apogee) ===
    # Fills up the first bar completely
    for i in range(laenge + 1):
        prozent = int((i / laenge) * 100)
        bar = "█" * i + "░" * (laenge - i)

        # Real-time flight phase text and delays for the ascent
        if prozent < 10:
            status_text = "Launch -> High-thrust propulsion burning...  "
            delay = 0.02 * SPEED_VIZ
        elif prozent < 25:
            status_text = "Burnout & rocket motors separated!          "
            delay = 0.15 * SPEED_VIZ
        elif prozent < 30:
            status_text = "DE-SPIN successful - Rotation 0 Hz          "
            delay = 0.15 * SPEED_VIZ
        else:
            status_text = "Microgravity phase active                   "
            delay = 0.12 * SPEED_VIZ

        # Output format: Text first, then the bar
        print(f"\rStatus UP   | {status_text} | [{bar}] {prozent:3}%", end="", flush=True)
        time.sleep(delay)

    # Brief pause at apogee (100%) and break to a new line for the descent bar
    time.sleep(0.5)
    print()

    # === Phase 2: DOWN (Descent to Earth) ===
    # A fresh second bar empties down below the first one
    for i in range(laenge, -1, -1):
        prozent = int((i / laenge) * 100)
        balken = "█" * i + "░" * (laenge - i)

        # Real-time flight phase text and delays for the descent
        if prozent > 30:
            status_text = "STATUS: Microgravity experiments running... "
            delay = 0.12 * SPEED_VIZ
        elif prozent == 0:
            status_text = "Landed - Helicopter for Recovery deployed!  "
            delay = 0.35 * SPEED_VIZ
        else:
            status_text = "Recovery-System deployed -> Parachute open  "
            delay = 0.35 * SPEED_VIZ

        # Overwrites only the second line, leaving the full UP bar intact above
        print(f"\rStatus DOWN | {status_text} | [{balken}] {prozent:3}%", end="", flush=True)
        time.sleep(delay)


def archive_mission_data(chosen_experiments: list, experimente_dict: dict, wind_speed: float):
    """
    Archives the operational flight data in compliance with FAIR RDM principles.
    Stores the structured dataset as a JSON file inside the /mission_archive directory.
    """

    # 1. Ensure the target archive directory exists if nit create one
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archive_dir =  os.path.join(script_dir, "mission_archive")

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Write the experiment log
    full_names_list = []
    for exp_key in chosen_experiments:
        if exp_key in experimente_dict:
            # EXPERIMENTE-Dict - >> Tupel Name is [1]
            full_name = experimente_dict[exp_key][1]
            full_names_list.append(full_name)

    # timestamp
    timestamp_file = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join( archive_dir, f"{timestamp_file}.json")

    # mission log
    mission_log = {
        "title": "Mission Report - MAPEUS",
        "timestamp": datetime.now().strftime("%Y%m%d-%H%M%S"),
        "launch_site": f"{LAUNCH_SITE_NAME} (Lat {LAUNCH_SITE_LAT}, Lon {LAUNCH_SITE_LON})",
        "environmental_conditions": {
            "wind_speed_kmh": wind_speed
        },
        "payload_manifest": {
            "total_modules": len(full_names_list),
            "deployed_experiments": full_names_list
        }
    }

    #write into a json-file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(mission_log, file, indent=4, ensure_ascii=False)
    return filename

if __name__ == "__main__":
    main()