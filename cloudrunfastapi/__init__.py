"""cloudrun-fastapi"""
import os

__version__ = os.getenv("API_TAG_VERSION", "0.1.0")
__project_id__ = os.getenv("PROJECT_ID", "local")
