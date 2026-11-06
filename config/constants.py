# ==========================================
#  config/constants.py
# ==========================================

MISSION_NAME = "Mapeus"           # To Do: user input at game start

# --- Rocket Base Configurations (e.g., MORABA MAPHEUS/MAPHEUS System)
ROCKET_BASE_INERTIA = 1.50      # kg*m^2 (Service + Recovery Module base)
ROCKET_BASE_MASS = 85.0         # kg (Dry mass of the launcher system)

# Maximum number of hardware slots allowed on the payload deck
MAX_PAYLOAD_SLOTS = 10

# Additional buffer slots available only on the workbench during the assembly process (non-permanent)
ASSEMBLY_BUFFER_SLOTS = 5

# Dynamically calculated baseline to guarantee flexibility across controllers and views
MAX_WORKBENCH_SLOTS = MAX_PAYLOAD_SLOTS + ASSEMBLY_BUFFER_SLOTS

# --- Science Payload Specifications
INERTIA_PER_BIO = 0.25          # kg*m^2 per biological module
INERTIA_PER_TEC = 0.50          # kg*m^2 per technological module

MASS_PER_BIO = 14.5             # kg per biological module
MASS_PER_TEC = 29.0             # kg per technological module


# --- Esrange Launch Site Config
LAUNCH_SITE_NAME = "Esrange, Sweden"
LAUNCH_SITE_LAT = 67.892
LAUNCH_SITE_LON = 21.106

# --- Yo-Yo De-Spin Mechanical Constraints
# Source: NASA Technical Note D-3848 / Esrange Sounding Rocket Safety Manual Sec. 4.2
MIN_WIRE_LENGTH = 0.80          # meters (Minimum deployment to clear rocket skin)
MAX_WIRE_LENGTH = 3.00          # meters (Maximum limit based on payload fairing volume clearance)

# Pre-defined game design values for inertia per module for easy player-calculation
INERTIA_PER_BIO = 0.25  #refactoring local var i_per_bio
INERTIA_PER_TEC = 0.50  #refactored local var i_per_tec

# --- Environmental Launch Constraints
# Source: MORABA Mission Operations Handbook - Surface Wind Limits
MAX_ALLOWABLE_WIND_SPEED = 30.0 # km/h (Safety threshold for active launcher adjustment)
DEFAULT_WIND_SPEED = 12.5       # km/h (Fallback standard velocity metric)

# --- UI & Visualization Settings
SPEED_VIZ = 2
TERMINAL_WIDTH = 80