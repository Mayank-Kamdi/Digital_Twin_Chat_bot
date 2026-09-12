import sys
import os
from pathlib import Path

# Explicitly add the project root to the Python path
# This prevents ModuleNotFoundError for 'backend' when Vercel runs this file
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.app import app
