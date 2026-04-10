"""
One-time preprocessing script for extracting and storing face embeddings.

This script:
1. Reads face images from faces_db/{person_name}/ structure
2. Computes embeddings for each face
3. Averages embeddings per person
4. Stores as pickle files in face_embeddings/
5. Updates metadata.json with person names

Usage:
    python -m scripts.extract_embeddings
"""
import cv2
import numpy as np
import os
import pickle
import json
from pathlib import Path
from app.services.face_model import initialize_face_analysis
from app.common.config import EMBEDDINGS_DIR, FACES_DB_DIR
from app.utils.logging import get_logger

logger = get_logger(__name__)

METADATA_FILE = EMBEDDINGS_DIR / "metadata.json"


def load_existing_metadata() -> list[str]:
    """
    Load existing metadata to check already processed persons.
    
    Returns:
        List of person names already processed
    """
    if METADATA_FILE.exists():
        try:
            with open(METADATA_FILE, "r") as f:
                data = json.load(f)
                return data.get("names", [])
        except Exception as e:
            logger.warning(f"Failed to load metadata: {e}")
    return []


def load_face_database() -> dict:
    """
    Load images for new persons and compute average embeddings.
    
    Returns:
        Dictionary mapping person names to their average embeddings
    """
    if not FACES_DB_DIR.exists():
        logger.error(f"Face database folder '{FACES_DB_DIR}' not found.")
        return {}
    
    # Load existing metadata to avoid reprocessing
    existing_names = set(load_existing_metadata())
    
    # Initialize face analyzer
    face_analyzer = initialize_face_analysis()
    
    known_faces = {}
    
    # Get list of new persons (folders not yet processed)
    person_folders = [
        p for p in os.listdir(FACES_DB_DIR)
        if os.path.isdir(os.path.join(FACES_DB_DIR, p)) and p not in existing_names
    ]
    total_persons = len(person_folders)
    
    if total_persons == 0:
        logger.info("No new persons to process")
        return {}
    
    logger.info(f"Processing {total_persons} new persons")
    
    for idx, person_name in enumerate(person_folders, start=1):
        person_path = os.path.join(FACES_DB_DIR, person_name)
        embeddings = []
        
        for image_file in os.listdir(person_path):
            image_path = os.path.join(person_path, image_file)
            
            try:
                image = cv2.imread(image_path)
                if image is None:
                    logger.warning(f"Unable to read {image_path}")
                    continue
                
                # Convert BGR to RGB (InsightFace expects RGB input)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                faces = face_analyzer.get(image)
                
                if len(faces) == 1:  # Use only images with exactly one face
                    embeddings.append(faces[0].embedding)
                else:
                    logger.debug(f"Skipping {image_path}: Found {len(faces)} faces")
            
            except Exception as e:
                logger.warning(f"Error processing {image_path}: {e}")
                continue
        
        if embeddings:
            # Compute the mean embedding
            avg_embedding = np.mean(embeddings, axis=0)
            known_faces[person_name] = avg_embedding
            logger.info(
                f"({idx}/{total_persons}) Stored embedding for {person_name} "
                f"({len(embeddings)} images)"
            )
        else:
            logger.warning(f"({idx}/{total_persons}) No valid images found for {person_name}")
    
    return known_faces


def save_embeddings(known_faces: dict) -> None:
    """
    Save computed embeddings and update metadata.
    
    Args:
        known_faces: Dictionary mapping names to embeddings
    """
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load existing metadata
    existing_names = set(load_existing_metadata())
    
    # Update metadata with new names
    updated_names = list(existing_names.union(known_faces.keys()))
    
    try:
        with open(METADATA_FILE, "w") as f:
            json.dump({"names": updated_names}, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save metadata: {e}")
        raise
    
    # Save each embedding
    for name, embedding in known_faces.items():
        embedding_path = EMBEDDINGS_DIR / f"{name.replace(' ', '_')}.pkl"
        try:
            with open(embedding_path, "wb") as f:
                pickle.dump(embedding, f)
            logger.debug(f"Saved embedding: {name}")
        except Exception as e:
            logger.error(f"Failed to save embedding for {name}: {e}")
            raise
    
    logger.info(f"Saved {len(known_faces)} new face embeddings to {EMBEDDINGS_DIR}")


def main() -> None:
    """Main execution function."""
    logger.info("Starting embedding extraction...")
    
    new_faces = load_face_database()
    
    if new_faces:
        save_embeddings(new_faces)
        logger.info("Embedding extraction completed successfully")
    else:
        logger.info("No new persons detected. Skipping extraction process.")


if __name__ == "__main__":
    main()
