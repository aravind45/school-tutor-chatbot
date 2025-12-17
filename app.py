"""
FastAPI Backend Server for Tutor Chatbot

Provides REST API endpoints for the web-based tutor chatbot interface.
"""

import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from model_service import ModelService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tutor Chatbot API",
    description="API for interacting with a fine-tuned Llama tutor model",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model service instance
model_service: Optional[ModelService] = None


# ============================================================================
# PYDANTIC DATA MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validate that message is not empty and within length limits"""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        if len(v) > 2000:
            raise ValueError('Message too long (max 2000 characters)')
        return v.strip()


class ChatResponse(BaseModel):
    """Response model for successful chat responses"""
    response: str
    status: str = "success"


class ErrorResponse(BaseModel):
    """Response model for error responses"""
    error: str
    status: str = "error"
    code: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    model_loaded: bool
    device: str
    gpu_name: Optional[str] = None
    gpu_memory_gb: Optional[float] = None


# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize the model service on startup"""
    global model_service
    
    try:
        logger.info("Starting up application...")
        
        # Get model path from environment or use default
        model_path = os.getenv("MODEL_PATH", "tutor_model_lora")
        max_seq_length = int(os.getenv("MAX_SEQ_LENGTH", "2048"))
        
        logger.info(f"Loading model from: {model_path}")
        model_service = ModelService(
            model_path=model_path,
            max_seq_length=max_seq_length
        )
        
        logger.info("✅ Application startup complete")
        
    except Exception as e:
        logger.error(f"Failed to initialize model service: {str(e)}")
        # Don't crash the app, but model won't be available
        model_service = None


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application...")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """
    Serve the frontend HTML page.
    
    Returns the static HTML file for the chat interface.
    """
    try:
        html_path = os.path.join("static", "index.html")
        
        if not os.path.exists(html_path):
            return HTMLResponse(
                content="<h1>Frontend not found</h1><p>Please create static/index.html</p>",
                status_code=404
            )
        
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"Error serving frontend: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load frontend")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return the tutor's response.
    
    Args:
        request: ChatRequest containing the user's message
        
    Returns:
        ChatResponse with the generated response
        
    Raises:
        HTTPException: If model is not loaded or generation fails
    """
    try:
        # Check if model service is available
        if model_service is None or not model_service.is_ready():
            raise HTTPException(
                status_code=503,
                detail="Model service is not available. Please try again later."
            )
        
        logger.info(f"Processing message: {request.message[:50]}...")
        
        # Generate response using model service
        response_text = model_service.get_response(
            user_message=request.message,
            max_tokens=500
        )
        
        logger.info(f"Generated response: {response_text[:50]}...")
        
        return ChatResponse(
            response=response_text,
            status="success"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message. Please try again."
        )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify server and model status.
    
    Returns:
        HealthResponse with server status and device information
    """
    try:
        if model_service is None:
            return HealthResponse(
                status="unhealthy",
                model_loaded=False,
                device="unknown"
            )
        
        device_info = model_service.get_device_info()
        
        return HealthResponse(
            status="healthy" if model_service.is_ready() else "unhealthy",
            model_loaded=device_info.get("model_loaded", False),
            device=device_info.get("device", "unknown"),
            gpu_name=device_info.get("gpu_name"),
            gpu_memory_gb=device_info.get("gpu_memory_gb")
        )
        
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return HealthResponse(
            status="error",
            model_loaded=False,
            device="unknown"
        )


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=400,
        content={
            "error": str(exc),
            "status": "error",
            "code": "VALIDATION_ERROR"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred",
            "status": "error",
            "code": "INTERNAL_ERROR"
        }
    )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    # Default to 7860 for Hugging Face Spaces compatibility
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "7860"))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=False,  # Set to True for development
        log_level="info"
    )
