import pickle
from tqdm import tqdm
from app.common.config import EMBEDDINGS_DIR
from app.utils.logging import get_logger

logger = get_logger(__name__)


def load_known_embeddings() -> dict:
    """
    Load all known face embeddings from disk.
    Searches for .pkl files in the embeddings directory.

    Returns:
        Dictionary mapping person names to embeddings (numpy arrays)
    """
    known_faces = {}

    if not EMBEDDINGS_DIR.exists():
        logger.info(f"Creating embeddings directory: {EMBEDDINGS_DIR}")
        EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
        return known_faces

    embedding_files = [file for file in EMBEDDINGS_DIR.iterdir() if file.suffix == ".pkl"]

    if not embedding_files:
        logger.warning("No embedding files found")
        return known_faces

    for file in tqdm(embedding_files, desc="Loading embeddings", unit="file"):
        try:
            person_name = file.stem
            with open(file, "rb") as f:
                embedding = pickle.load(f)
            known_faces[person_name] = embedding
        except Exception as e:
            logger.warning(f"Failed to load embedding from {file}: {e}")

    logger.info(f"Loaded {len(known_faces)} face embeddings successfully")
    return known_faces


def save_embedding(person_name: str, embedding) -> None:
    """
    Save a single face embedding to disk.

    Args:
        person_name: Name of the person
        embedding: Numpy array containing the face embedding
    """
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = person_name.replace(" ", "_")
    embedding_path = EMBEDDINGS_DIR / f"{safe_name}.pkl"

    try:
        with open(embedding_path, "wb") as f:
            pickle.dump(embedding, f)
        logger.debug(f"Saved embedding for: {person_name}")
    except Exception as e:
        logger.error(f"Failed to save embedding for {person_name}: {e}")
        raise