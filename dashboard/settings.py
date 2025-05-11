import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "dashboard" / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
MOCK_DATA_DIR = ASSETS_DIR / "mock_data"

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "dev_default_secret_key_not_for_production")
HASH_ITERATIONS = 260000  # For PBKDF2 password hashing

# OpenRouter.ai API settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Session management
SESSION_TIMEOUT_MINUTES = 60

# Feature flags
ENABLE_AI_FEATURES = bool(OPENROUTER_API_KEY)
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "True").lower() == "true"

# Memory store settings
MAX_CAMPAIGNS_PER_USER = 100
MAX_USERS = 1000
