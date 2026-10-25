import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deployment")
    DATABASE = os.environ.get("GYM_DATABASE", str(BASE_DIR / "gym_management.db"))
