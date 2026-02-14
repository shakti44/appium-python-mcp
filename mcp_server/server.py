"""FastAPI MCP server for mobile automation."""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
from utils.logger import setup_logger, logger
from config.environment import settings
from mcp_server.handlers import MCPHandlers
from mcp_server.schemas import *


# Setup logging
logger = setup_logger(
    level=settings.log_level,
    log_file=settings.log_file if settings.log_file else None
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting Appium MCP Server...")
    logger.info(f"Server configuration:")
    logger.info(f"  Host: {settings.server_host}")
    logger.info(f"  Port: {settings.server_port}")
    logger.info(f"  Appium URL: {settings.appium_server_url}")
    
    yield
    
    logger.info("Shutting down Appium MCP Server...")
    # Cleanup sessions on shutdown
    if hasattr(app.state, 'handlers'):
        app.state.handlers.session_manager.delete_all_sessions()


# Create FastAPI application
app = FastAPI(
    title="Appium MCP Server",
    description="AI-driven MCP-compatible mobile automation server",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize handlers
handlers = MCPHandlers()
app.state.handlers = handlers


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            message=str(exc),
            timestamp=datetime.now().isoformat()
        ).dict()
    )


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return await handlers.health_check()


@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message
    """
    return {
        "message": "Appium MCP Server",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Session endpoints
@app.post("/sessions", response_model=SessionCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_session(request: SessionCreateRequest):
    """
    Create a new Appium session.
    
    Args:
        request: Session creation request
        
    Returns:
        Session creation response
    """
    try:
        return await handlers.create_session(request)
    except Exception as e:
        logger.error(f"Session creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/sessions", response_model=Dict[str, SessionInfo])
async def list_sessions():
    """
    List all active sessions.
    
    Returns:
        Dictionary of session IDs to session info
    """
    return await handlers.list_sessions()


@app.get("/sessions/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
    """
    Get session information.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Session information
    """
    try:
        return await handlers.get_session(session_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Deletion result
    """
    return await handlers.delete_session(session_id)


# Command execution endpoints
@app.post("/commands", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute a natural language command.
    
    Args:
        request: Command request
        
    Returns:
        Command execution result
    """
    return await handlers.execute_command(request)


@app.post("/elements/action", response_model=CommandResponse)
async def execute_element_action(request: ElementActionRequest):
    """
    Execute an element action.
    
    Args:
        request: Element action request
        
    Returns:
        Action execution result
    """
    return await handlers.execute_element_action(request)


@app.post("/gestures", response_model=CommandResponse)
async def execute_gesture(request: GestureRequest):
    """
    Execute a gesture.
    
    Args:
        request: Gesture request
        
    Returns:
        Gesture execution result
    """
    return await handlers.execute_gesture(request)


# Screenshot endpoint
@app.post("/screenshots", response_model=ScreenshotResponse)
async def take_screenshot(request: ScreenshotRequest):
    """
    Take a screenshot.
    
    Args:
        request: Screenshot request
        
    Returns:
        Screenshot response with path
    """
    try:
        return await handlers.take_screenshot(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# Code generation endpoints
@app.post("/generate/test", response_model=TestGenerationResponse)
async def generate_test(request: TestGenerationRequest):
    """
    Generate test code from commands.
    
    Args:
        request: Test generation request
        
    Returns:
        Generated test code
    """
    return await handlers.generate_test(request)


@app.post("/generate/page-object", response_model=PageObjectGenerationResponse)
async def generate_page_object(request: PageObjectGenerationRequest):
    """
    Generate page object code.
    
    Args:
        request: Page object generation request
        
    Returns:
        Generated page object code
    """
    return await handlers.generate_page_object(request)


def start_server(host: str = None, port: int = None):
    """
    Start the MCP server.
    
    Args:
        host: Server host (defaults to settings)
        port: Server port (defaults to settings)
    """
    import uvicorn
    
    host = host or settings.server_host
    port = port or settings.server_port
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    start_server()
