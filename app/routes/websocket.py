import json
import numpy as np
from fastapi import WebSocket, WebSocketDisconnect
from app.services.recognition import recognition_system
from app.utils.logging import get_logger
from app.utils.image import decode_frame_from_bytes
from app.schemas.recognition import FaceLabel, ErrorResponse

logger = get_logger(__name__)


async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for real-time face recognition.
    
    Process flow:
    1. Accept client connection
    2. Receive image frames as bytes
    3. Process frames for face detection and recognition
    4. Send responses with recognized faces
    5. Handle disconnection
    
    Args:
        websocket: WebSocket connection instance
    """
    await websocket.accept()
    logger.info("Client connected to WebSocket")
    
    try:
        while True:
            # Receive image frame as bytes
            data = await websocket.receive_bytes()
            
            # Decode frame from bytes
            frame = decode_frame_from_bytes(data)
            if frame is None:
                error = ErrorResponse(
                    error="Failed to decode image",
                    code=422
                )
                await websocket.send_text(error.model_dump_json())
                continue
            
            # Process frame for face detection and recognition
            faces = recognition_system.process_frame(frame)
            
            # Format response
            if not faces:
                error = ErrorResponse(
                    error="No valid face detected",
                    code=404
                )
                await websocket.send_text(error.model_dump_json())
                continue
            
            # Send recognized faces
            face_data = [FaceLabel(label=face.label) for face in faces]
            response = [face.model_dump() for face in face_data]
            logger.info(f"Detected {len(response)} faces: {response}")
            await websocket.send_text(json.dumps(response))
    
    except WebSocketDisconnect:
        logger.info("Client disconnected from WebSocket")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        error = ErrorResponse(
            error=f"Internal Server Error: {str(e)}",
            code=500
        )
        try:
            await websocket.send_text(error.model_dump_json())
        except Exception:
            pass
