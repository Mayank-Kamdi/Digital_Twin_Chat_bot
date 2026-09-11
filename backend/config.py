"""Configuration and environment variables management."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

# Load .env file
load_dotenv(dotenv_path=ENV_PATH)

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1").strip()
PORT = int(os.getenv("PORT", "8000"))

# RAG & Retrieval configuration
TOP_K_CHUNKS = int(os.getenv("TOP_K_CHUNKS", "4"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.15"))

# Application Metadata
APP_NAME = "LYRA Digital Twin"
APP_VERSION = "1.0.0"
