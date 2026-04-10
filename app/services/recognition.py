import numpy as np
import cv2
from insightface.app import FaceAnalysis
from app.services.face_model import initialize_face_analysis
from app.services.embeddings import load_known_embeddings
from app.utils.logging import get_logger
from app.utils.image import resize_frame

logger = get_logger(__name__)

class Face:
    def __init__(self, bbox, embedding, label):
        self.bbox = bbox
        self.embedding = embedding
        self.label = label


class FaceRecognitionSystem:
    def __init__(self):
        self.detection: FaceAnalysis | None = None
        self.known_faces: dict = {}
        self._initialize()
    
    def _initialize(self) -> None:
        try:
            self.detection = initialize_face_analysis()
            self.known_faces = load_known_embeddings()
            logger.info(
                f"FaceRecognitionSystem initialized with "
                f"{len(self.known_faces)} known faces"
            )
        except Exception as e:
            logger.error(f"FaceRecognitionSystem initialization failed: {e}")
            self.known_faces = {}
            self.detection = None
    
    def recognize_face(self, embedding: np.ndarray) -> tuple[str, float]:
        if not self.known_faces:
            return "Unknown", 0
        
        best_match = None
        best_score = -1
        
        # Compute cosine similarity with all known faces
        for name, ref_embedding in self.known_faces.items():
            similarity = np.dot(embedding, ref_embedding) / (
                np.linalg.norm(embedding) * np.linalg.norm(ref_embedding)
            )
            if similarity > best_score:
                best_score = similarity
                best_match = name
        
        # Convert similarity score to confidence percentage
        confidence = (best_score + 1) / 2 * 100
        
        # Check if score exceeds threshold
        if best_score > 0.5:
            return best_match, confidence
        else:
            return "Unknown", confidence
    
    def process_frame(self, frame: np.ndarray) -> list[Face]:
        if self.detection is None:
            logger.warning("Detection model not initialized")
            return []
        
        try:
            # Resize frame for faster processing
            small_frame = resize_frame(frame, 0.5)
            
            # Detect faces using InsightFace
            detected_faces = self.detection.get(small_frame)
            
            # Sort faces by size (largest first)
            detected_faces.sort(
                key=lambda face: (face.bbox[2] - face.bbox[0]) * (face.bbox[3] - face.bbox[1]),
                reverse=True
            )
            
            # Recognize each face and assign label
            result_faces = []
            for face in detected_faces:
                label, confidence = self.recognize_face(face.embedding)
                result_face = Face(
                    bbox=face.bbox,
                    embedding=face.embedding,
                    label=label
                )
                result_faces.append(result_face)
            
            logger.debug(f"Detected {len(result_faces)} faces")
            return result_faces
        
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return []


recognition_system = FaceRecognitionSystem()
