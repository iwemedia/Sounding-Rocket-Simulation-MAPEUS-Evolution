# 🚀 MAPEUS Sounding Rocket Simulator (OOP-MVC Refactored)

An interactive command-line mission control text adventure and rocket science simulator, inspired by the 
real-world **MORABA MAPHEUS Missions** executed by the German Aerospace Center (DLR).

---

## 💡 Inspiration & Motivation

The core motivation behind this project is deeply personal. I had the unique opportunity to 
visit the **MORABA (Mobile Rocket Base)** team at the **German Aerospace Center (DLR) in Oberpfaffenhofen**. 
During this visit, I conducted **8 extensive interviews** with the team members, focusing heavily on the 
theme *"How to build a rocket and fly"*, with a special emphasis on making **Women in Science and Technology** 
visible in their engineering excellence. This resulted in the dedicated **Podcast: Scienckompass *inSTEM***.

The invaluable insights, practical challenges, and systems engineering principles shared by these scientists, 
mechanics, and aerospace engineers are the foundational backbone of this simulator. 
While the real-world **MAPHEUS** research campaigns serve as the direct scientific inspiration, this independent 
simulation game is officially titled **MAPEUS**. This project aims to transform real-world campaign experiences 
into a playful, educational interactive adventure, making complex multi-stage campaign planning visible and 
accessible to everyone. By simulating the constraints and decisions faced in real suborbital campaigns, this 
project honors their work and promotes the crucial role of women in aerospace engineering and space exploration.

---

## Project Overview & Core Concept

Every research rocket is unique. Sounding rockets are modular, custom-built hardware stacks designed to carry varying 
scientific experiments into microgravity by executing a precise parabolic flight trajectory. 

The **MAPEUS Simulator** challenges the player to take on the role of an Aerospace Engineer and Mission Manager. 
The primary goal is to assemble and safely guide a suborbital rocket through a sequence of engineering, physical, 
and environmental checkpoints to achieve a "VALID MISSION" status, maximize microgravity conditions for scientists, 
and safely archive the research data.

### Educational Value & Real-World Skills
This project acts as an educational intersection of project management, scientific communication, systems engineering, 
flight dynamics, and real-world API data integration:
* **Systems Engineering:** Managing rigid physical hardware decks and understanding how individual experiment 
module selections alter the total vehicle mass and configuration.
* **Flight Physics:** Understanding spin-stabilization and the mechanical dynamics required to cancel 
centrifugal forces via deployment cables to achieve near 0 Hz rotation.
* **Data Integration:** Fetching live meteorological telemetry from a remote REST API to dynamically 
evaluate launch safety constraints.

---

## 📐 Scientific Formulas & In-Game Rules

To maintain the spirit of a true rocket campaign while keeping the user experience accessible, the suborbital 
calculations were scaled down to focused, intuitive core mechanics:

### 1. Yo-Yo Despin Balances (Phase 2)
To deploy the chosen experiments safely under microgravity conditions, the rocket's high 
rotational velocity (approx. 4 Hz) must be reduced to approximately 0 Hz. 
This is achieved by deploying two mechanical counterweights on extendable wires (Yo-Yo Despin System). 
The game calculates the precise weight per Yo-Yo mass (m) using a 
relationship derived from **NASA Technical Note D-3848**, based on the total moment of 
inertia (\(I_{\text{total}}\)) and the user-selected deployment cable length (L):

\[m = \frac{I_{\text{total}}}{L^2}]

The player must choose a safe wire length between 0.80 m and 3.00 m and successfully identify the correct 
mathematically approximated weight from a shuffled list to clear the engineering phase.

### 2. Environmental Launch Constraints (Phase 3)
The live environment is checked by querying the remote **Open-Meteo REST API** using the actual geographical 
coordinates of the **Esrange Launch Site** in Kiruna, Sweden (67.892° N, 21.106° E). 
If the real-time surface wind speed exceeds the safety threshold of **30.0 km/h**, 
the launch is automatically scrubbed.

---

## 🏗️ Architectural Evolution: The Shift to OOP & MVC

### From Monolith to Clean Separation
In its initial version, the simulator was built as a monolithic script where data management, UI presentation, and 
campaign orchestration were tightly coupled. 

In this **major architectural refactoring phase**, the monolith was completely dissolved and rebuilt from 
scratch following the **Model-View-Controller (MVC)** design pattern and strict Object-Oriented Programming (OOP) 
principles to power the **MAPEUS** engine:

* **The Model (`models/`):** Encapsulates core state and domain logic. `Module` represents a single experiment entry, 
while `Rocket` handles the physical hardware grid, executes gap-closing operations, and tracks active flight metrics.
* **The View (`views/`):** The `TerminalView` class serves as the **exclusive interface** to the player. 
It encapsulates all I/O operations (`print`, `rich.panel`, `input`, ASCII banners). The remaining codebase has no 
dependencies on terminal drawing mechanics.
* **The Controller (`controllers/`):** The `GameController` class acts as the primary conductor of the campaign 
timeline. It retrieves data from models/services, passes layout states to the view, and routes user interactions. 
* **It is 100% free of direct I/O execution.**

### Centralized Balance (Single Source of Truth)
Instead of hardcoding system constants throughout the script, variables like the 
vehicle dry mass (`ROCKET_BASE_MASS`), structural inertia (`ROCKET_BASE_INERTIA`), and the dynamically 
computed workbench deck buffer capacity (`MAX_WORKBENCH_SLOTS`) are centralized in the configuration facade layer.

### State-Driven Orchestration (The State Pattern Blueprint)
To prevent the `GameController` from becoming a bloated state machine or relying on primitive local integers to track 
timeline progression, the campaign's lifecycle is encapsulated within a dedicated `Mission` state model. 
This architectural choice implements a foundational blueprint of the **State Pattern**:
* `self.current_phase`: Encapsulates the exact global state of the mission profile in memory (Phases 0 to 5). 
It isolates chronological phase-transitions from the central control flow, enabling separate layers 
(like Views or Services) to dynamically query the active checkpoint.
* `self.is_valid_mission`: Functions as a centralized boolean safety flag ("Go / No-Go" matrix indicator). 
It decouples the business logic of environmental and structural constraints (such as API-verified crosswinds or workbench buffer violations) from the orchestrator. If bounds are breached, this state is invalidated, routing the system into recovery contexts and serializing directly into the FAIR-RDM post-flight logs.

---

## 📂 File Structure

```text

├── requirements.txt       # Centralized package dependencies registry (rich, requests, etc.)
├── architecture.md        # Complete technical UML class diagram documentation
├── README.md              # This core project documentation
│
├── project.py             # Ultra-lean bootstrapper script (Central entrance hook)
│
├── config/
│   ├── constants.py                    # Centralized game balance & physical constants (SSOT)
│   └── catalog.py                      # Hardware catalog for available scientific modules
│
├── controllers/
│   └── game_controller.py              # Campaign orchestrator engine driving Phases 0 to 5 (Pure Logic)
│
├── views/
│   ├── terminal_view.py                # Exclusive presentation layer (Rich UI, inputs, animation buffers)
│
├── models/
│   ├── mission.py                      # decoupling state from logic **State Pattern** creates sequence of readable state transitions
│   ├── module.py                       # Domain model encapsulating single experiment parameters
│   └── rocket.py                       # State model managing payload stack allocations & gap closures
│
├── physics/
│   ├── de_spin_calculator.py           # NASA Yo-Yo wire dynamics constraints checking
│   └── mass_properties_calculator.py   # Standalone math engine for inertia matrices
│
├── services/
│   ├── weather_service.py # Network client for live Open-Meteo REST API fetching
│   └── archive_service.py # Persistent, FAIR-compliant JSON data archiving snapshotter
│
└── mission_archive                     # dynamically generated
   
```

> 📊 **UML Class Diagram:** A fully detailed, zoomable architectural class diagram mapping all method 
signatures and properties can be viewed interactively in the browser:
> 👉 **[View MAPEUS Architecture Diagram in Fullscreen](https://tinyurl.com/mermaidUMLrefactorMMM)**

---

## 🛠️ Lessons Learned & Engineering Insights

1. **The Architectural Design Patterns Triumph (MVC, State & Facade)**
   Moving away from the single-file monolith highlighted the immense practical value of enterprise design patterns. 
Orchestrating a clean **Model-View-Controller (MVC)** split successfully isolated tricky terminal presentation 
behaviors (like `rich.columns` tracking and real-time carriage-return flushing inside the `launch_status_bar`) 
from baseline control routing. 
Furthermore, decoupling state from logic via the **State Pattern** (`Mission` class) eliminated hardcoded loop hacks 
and structural wiggles, turning the campaign into an elegant sequence of readable state transitions. 
Finally, leveraging the **Facade Pattern** inside package boundaries (such as `physics/__init__.py` 
using explicit `__all__` interface exposures) hid internal math complexities, providing clean interaction APIs for the orchestrator layer and preventing static analysis warnings.


2. **API Identity Verification & User-Agent Spoofing**
   During Phase 3 development, the remote Open-Meteo REST API continuously rejected automated script headers, 
throwing connection blockers. By researching client signatures, a structured identity dictionary was injected 
(`headers = {"User-Agent": "..."}`), successfully authorizing the ground console simulation as a realistic browser 
session.

3. **Silent Exception Triggers & Strict Data Contracts**
   To prevent malformed JSON responses from crashing flight operations, explicit key-existence audits were 
introduced inside the data parsing pipeline prior to executing float castings. If the API feed drops, a robust fallback mechanism seamlessly deploys the centralized `DEFAULT_WIND_SPEED`.

4. **Regional Typography Mapping & Data Integrity**
   Designing an engineering simulator required strict control over decimal boundaries. Custom input validation 
sanitizers were built to catch regional formatting anomalies—such as European operators typing a comma `,` instead 
of a standard mathematical decimal dot `.`—shielding the calculation loops from runtime crashes.
