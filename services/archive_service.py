# services/archive_service.py
import json
import os
from datetime import datetime
from config.constants import LAUNCH_SITE_NAME, MISSION_NAME

def archive_mission(rocket_object, wind_speed: float, success: bool, archive_dir: str = "archive") -> str:
    """
    Handles the persistent FAIR-RDM archiving of mission data.
    Extracts explicit tracking IDs (e.g., BIO-01, TEC-01) from the finalized rocket object
    and exports a standardized JSON snapshot of the flight configuration.

    Args:
        rocket_object (Rocket): The finalized Rocket model instance containing active payload states.
        wind_speed (float): The validated surface wind speed velocity metric in km/h.
        success (bool): Flag indicating the chronological mission trajectory outcome status.
        archive_dir (str, optional): The target storage directory path. Defaults to "archive".

    Returns:
        str: The persistent absolute or relative file path configuration to the saved JSON audit log.
    """
    # Ensure the target directory infrastructure exists safely
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Generate an audit-trail timestamp for the file blueprint
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mission_{timestamp}.json"
    filepath = os.path.join(archive_dir, filename)

    # Extract active hardware modules by runtime instance tracking IDs
    # no gaps (NONE) -> maps the modules directly into the payload snapshot array
    payload_snapshot = [
        {
            "tracking_id": module.instance_id,
            "catalog_key": module.key,
            "name": module.name,
            "mass_kg": module.mass,
            "type": module.type
        }
        for module in rocket_object.modules
    ]

    # Standardized FAIR-RDM metadata registry block
    metadata = {
        "metadata_standard": f"FAIR-RDM-{MISSION_NAME}-v1.0",
        "timestamp": datetime.now().isoformat(),
        "launch_site": LAUNCH_SITE_NAME,
        "environment": {
            "wind_speed_kmh": wind_speed
        },
        "rocket_metrics": {
            "total_mass_kg": rocket_object.total_mass,
            "total_inertia_kgm2": rocket_object.total_inertia,
            "module_count": len(payload_snapshot)
        },
        "payload_configuration": payload_snapshot,
        "outcome": {
            "success": success
        }
    }

    # "Write-to-Temp-and-Rename" - Generate path for a temporary intermediate file layout
    temp_filepath = filepath + ".tmp"

    # Atomic write standard payload configuration data array to persistent storage
    with open(temp_filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    #  Execute the atomic file system rename to commit the temporary file to its final target path
    os.replace(temp_filepath, filepath)

    return filepath
