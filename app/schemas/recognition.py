from pydantic import BaseModel, Field

class FaceLabel(BaseModel):
    label: str = Field(..., description="Name of the recognized person or 'Unknown'")

    class Config:
        json_schema_extra = {
            "example": {"label": "john"}
        }

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    code: int = Field(..., description="Error code")

    class Config:
        json_schema_extra = {
            "example": {"error": "Failed to decode image", "code": 422}
        }
