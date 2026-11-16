
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Trailblazer profile
PROFILE_NAME = "Chiara Tardioli"
PROFILE_URL = "https://www.salesforce.com/trailblazer/chiarat"

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Output filenames
PROFILE_TEXT_FILE = RAW_DATA_DIR / "trailblazer_profile.txt"
API_JSON_FILE = RAW_DATA_DIR / "trailblazer_api.json"

CSV_OUTPUT_FILE = (
    PROCESSED_DATA_DIR /
    "chiara_tardioli_certifications.csv"
)

EXCEL_OUTPUT_FILE = (
    PROCESSED_DATA_DIR /
    "chiara_tardioli_certifications.xlsx"
)

# Browser configuration
HEADLESS = True
PAGE_TIMEOUT = 60000
WAIT_AFTER_LOAD = 7000


def create_directories():
    """Create required data directories."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

