import cv2
import numpy as np

def decode_frame_from_bytes(data: bytes) -> np.ndarray | None:
    try:
        frame = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        return frame
    except Exception:
        return None


def resize_frame(frame: np.ndarray, scale_factor: float) -> np.ndarray:
    return cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)
