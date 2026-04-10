from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from app.routes.websocket import websocket_endpoint
from app.services.recognition import recognition_system
from app.utils.logging import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="FaceServer API",
        version="2.0",
        description="Real-time face recognition server with WebSocket support"
    )
    
    @app.get("/")
    async def status() -> JSONResponse:
        num_identities = len(recognition_system.known_faces)
        logger.info(f"Status check: {num_identities} known faces available")
        
        if num_identities == 0:
            return JSONResponse(
                status_code=503,
                content={
                    "status_message": "Server not ready. No available faces found, please upload.",
                    "no_faces_uploaded": 0
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "Face Recognition Server is running",
                "faces_uploaded_count": num_identities
            }
        )
    
    @app.websocket("/ws")
    async def websocket_route(websocket: WebSocket) -> None:
        """
        WebSocket endpoint for real-time face recognition.
        
        - Accepts binary image frames
        - Returns JSON array of recognized faces
        - Each face: {"label": "person_name"}
        """
        await websocket_endpoint(websocket)
    
    return app

app = create_app()
