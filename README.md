#### an interactive command line text adventure and rocket science simulator
#### inspired by the real-world MORABA.de MAPHEUS-17-Mission 2026

# SOUNDING-ROCKET: Mission Manager Simulator 
## or "How to build a rocket and fly"
### Video Demo: 
#### Description: An interactive command-line mission control simulation 
#### inspired by the real-world MAPHEUS research campaigns executed by MORABA.de (Mobile Rocket Base / DLR Germany) 
#### and the Esrange Space Center in Kiruna, Sweden (ssc Sweden).

---

## 💡 Inspiration & Motivation

The core motivation behind this project is deeply personal. I had the unique opportunity to visit 
the **MORABA (Mobile Rocket Base)** team at the **German Aerospace Center (DLR) in Oberpfaffenhofen** this year.
During this visit, I conducted **8 extensive interviews** with the team members, focusing heavily on the 
theme *"How to build a rocket and fly"*, with a special emphasis on making **Women in Science and Technology** visible 
in there excellence -> **Podcast: Scienckompass *inSTEM**,

The invaluable insights, challenges, and engineering principles shared by these scientists, mechanics and engineers 
are the foundational backbone of this simulator. My goal was to transform their real-world experiences into a playful, 
educational interactive adventure, making the complex multi-stage campaign planning and scientific mission steps 
visible and accessible to everyone. By simulating the constraints and decisions they face in real campaigns, 
this project honors their work and promotes the crucial role of women in aerospace engineering and space exploration.

---

## Project Overview & Core Concept

Every research rocket is unique. Unlike commercial launch vehicles, sounding rockets are modular, custom-built 
stacks designed to carry varying scientific experiments into microgravity by executing an parabolic flight. 

The **SOUNDING-ROCKET: Mission Manager Simulator** challenges the player to take on the role of an Engineer and Mission Manager. 
The primary goal is to assemble and safely guide a suborbital rocket through a sequence of engineering and environmental 
checkpoints to achieve a "VALID MISSION" status, maximize microgravity conditions for scientists, 
and safely archive the research data and housekeeping data.

### Educational Value
This project acts as an educational intersection of project management and skills like scientific communication, 
systems engineering, flight dynamics, and real-world API data integration. 

Players learn about:
* **Systems Engineering:** 
* Managing strict hardware slots and understanding how experiment selection influences total vehicle mass.
* **Flight Physics:** 
* Understanding spin-stabilization and the mechanics required to cancel centrifugal forces to achieve near 0 Hz rotation.
* **Data Integration:** 
* Fetching real-time weather telemetry from a live REST API to evaluate launch constraints.
---

## 📐 Scientific Formulas & In-Game Rules

To maintain the spirit of a true rocket campaign while keeping the user experience accessible, 
the suborbital physics calculations were scaled down to focused, intuitive core mechanics:

### 1. Yo-Yo Despin Balances (Phase 2 Quiz)
To deploy the chosen experiments safely, the rocket's high rotational velocity must be reduced to approximately 0 Hz. 
This is achieved by deploying two mechanical counterweights on extendable wires. 
The game calculates the precise weight per Yo-Yo mass ($m$) using a simplified relationship derived from 
NASA Technical Note D-3848, based on the total moment of inertia ,
and by using some base_mass/inhertia approximations based on the MORABA MAPHEUS Missions.

(rocket base and scientific payload) 
($I_{\text{total}}$) 

and 

the user-selected deployment cable length ($L$):

$$m = \frac{I_{\text{total}}}{L^2 \times 2}$$

The player must choose a safe wire length between 0.80 m and 3.00 m and successfully identify the correct mathematically 
approximated weight from a shuffled list to clear the engineering phase.

### 2. Microgravity Metric & Telemetry Assessment (Phase 3 & 5)
In the background, the flight duration and scientific yield scale dynamically based on the weight configuration. 
The live environment is checked by querying the remote Open-Meteo REST API using the actual geographical coordinates 
of the **Esrange Launch Site** in Kiruna, Sweden (67.892° N, 21.106° E). 

If the real-time surface wind speed exceeds 30.0 km/h, the launch is automatically scrubbed for safety reasons. 
If conditions are nominal, the flight triggers an asynchronous double-status bar (Ascent and Descent) before compiling 
a final flight log.


---

## Project Idea, Scope Shifts & Design Decisions

### The Architecture vs. CS50 Rules
The original architecture of this project was intended to be a fully modular software framework, 
separating data models, terminal viewports, and narrative briefings into independent Python modules. 

However, to strictly comply with the **CS50P submission requirements** (which dictate a single, 
comprehensive `project.py` entry point accompanied by an automated `test_project.py` suite), 
the structural design was streamlined. 
The modular mindset was preserved internally: code blocks are strictly isolated by functionality, 
clean state variables manage the UI flow.
Data layers - like the `EXPERIMENTE` dictionary - are separated from the execution logic to ensure parts 
remain testable via `pytest`.

### Scope Simplifications (Vision vs. Reality)
To meet tight project deadlines and focus on code stability, several advanced launch variabeles were simplified or 
automated in the background:
* **Experiment Dependencies:** 
* Mutually exclusive hardware combinations were omitted; the mass is calculated completely in the 
* background based on the payload stack.
* **Motor Matching:** 
* Rocket motor stages are not assigned and given as a standard configuration.
* **Launcher Orientation:** 
* The aerodynamic tracking and manual rail angle alignment based on crosswinds were abstracted 
* into automated telemetry checks. 

---

## File Structure 

### 1. `project.py`
The brain of the application: contains the central loop, user configuration panels and backend 
physics calculators. 

It relies on the following custom functions:
*   `clear_screen()`: 
Cleans the terminal viewport interface using `subprocess` context calls depending on whether 
the host machine runs on Windows (`nt`) or UNIX environments.

*   `start_payload_stack(experimente)`: 
Manages the custom dual-panel terminal interface using `rich.columns`. 
It isolates the hardware constraints by limiting total loaded modules to 10 slots and sanitizing 
string inputs (`NEXT`, `REMOVE`, or experiment keys).

*   `calculate_rocket_configuration(n_bio, n_tec)`: 
Handles the vehicle systems engineering math. 
It aggregates mass layers and applies pre-defined game design constants to establish total moments of inertia 
($I_{\text{total}}$) for the combined suborbital stack.

*   `run_despin_quiz(i_total)`: 
Acts as an interactive numerical gate for Phase 2. 
It checks that the player type proper floating-point values (filtering out comma vs. dot variations) and 
applies NASA wire dynamics formulas.

*   `fetch_weather_data(lat, lon)`: 
Manages external REST API connections. 
It passes coordinates as isolated payload arguments and 
injects a custom identity header sequence (User-Agent spoofing) to prevent automated request blocking.

*   `extract_wind_speed(weather_data)`: 
Validates the data contract returned from external servers. 
It executes key-existence audits prior to running float conversions, shielding the runtime application from crashing.

*   `launch_status_bar(laenge)`: 
Animates as a dual bar, the real-time, asynchronous progressive status updates (Ascent to apogee and Descent to earth). 
Utilizes customized printing flush buffers.

*   `archive_mission_data(...)`: 
Implements data integrity patterns by serializing verified flight logs into structured JSON configurations with 
timestamps, saved in an automatically generated mission directory.

### 2. `test_project.py`

The automated testing suite validates the calculation engines and 
data extraction contracts against boundary limits and malformed inputs using `pytest`. 

It covers:
*   `test_calculate_rocket_configuration()`: 
Asserts happy-path calculations for exact total system inertia and combined 
liftoff mass vectors based on module distribution inputs.

*   `test_run_despin_quiz_edge_cases()`: 
Leverages `unittest.mock.patch` to simulate iterative console inputs, verifying that out-of-bounds wire 
length entries (e.g., 0.50m or 4.00m) are rejected while valid lengths resolve accurately.

*   `test_extract_wind_speed()` and `test_extract_wind_speed_malformed_data()`: 
Validates robust API contract failure handling by evaluating standart payloads, empty dictionaries, 
non-numeric strings (e.g., `"STORM"`), or missing target keys,
provides a fallback to `DEFAULT_WIND_SPEED`.

*   `test_archive_mission_data()`: 
Checks OS file generation and file existence, 
ensuring data serialization correctly stores active experimental arrays in standard JSON format.

### 3. `requirements.txt and Extras

* **`requirements.txt`**: 
Declares external packages used for advanced terminal styling (`rich`), ASCII title art (`pyfiglet`), 
and API networking (`requests`).

* **`run_game.bat`**:
A custom Windows batch script designed to boot up the simulator smoothly using the 
local isolated virtual environment (`venv`).

---

## Lessons Learned

Realizing this simulator brought several engineering challenges that requiered some 
problem-solving techniques in syntax:

1. **The Joy and Pain of Terminal UI (Rich Panels & Progress Bars)**
   Designing an retro mission-control experience inside a standard command-line interface was a bittersweet engineering 
   challenge. Utilizing the `rich` library to build side-by-side inventory panels (`Columns`) and multi-line, 
   asynchronous loading indicators (`launch_status_bar`) brought both immense joy and technical frustration. 
   Managing terminal widths, handling screen-flushes with `subprocess.run()`, and synchronizing real-time 
   print buffers without flickering .. a lot of timing and formatting.

2. **Overcoming API Request Blocking (User-Agent Spoofing)**
   During Phase 3 development, the remote Open-Meteo REST API continuously rejected automated connection 
   requests from the simulation script, threatening to break the live telemetry system. 
   By researching HTTP request headers, I implemented a custom identity signature (`headers = {"User-Agent": "..."}`) 
   that mimics a standard web browser session. This successfully authorized the automated scripts to sync real-time 
   weather metrics without continuous fallbacks.
   
3. **Robust API Data Contract Validation**
   To prevent the program from crashing on malformed JSON packages from external servers, I implemented explicit 
   key-existence audits (`if "current" in weather_data:`) before executing structural type castings 
   to insulated the data processing pipeline from runtime exceptions.

4. **Data Integrity & UX Error Handling**
   I gained appreciation for sanitizing user inputs. Since engineering parameters depend on decimal numbers, 
   I built custom exceptions to filter out regional formatting issues 
   (such as users typing a German comma `,` instead of a decimal dot `.`) to ensure the mathematical 
   operations run smoothly without system crashes.
