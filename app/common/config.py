import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
EMBEDDINGS_DIR = BASE_DIR / "face_embeddings"
FACES_DB_DIR = BASE_DIR / "faces_db"
