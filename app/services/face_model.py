from insightface.app import FaceAnalysis
from app.utils.logging import get_logger

logger = get_logger(__name__)

def initialize_face_analysis() -> FaceAnalysis:
    try:
        face_analyzer = FaceAnalysis(
            name="buffalo_s",
            providers=["CPUExecutionProvider"],
            allowed_modules=['detection', 'recognition']
        )
        face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
        logger.info(f"Face analysis model initialized with \"buffalo_s\" model")
        return face_analyzer
    except Exception as e:
        logger.error(f"Failed to initialize face analysis: {e}")
        raise
