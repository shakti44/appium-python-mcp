"""FastAPI MCP Server implementation for Appium automation."""
import json
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import logging
from datetime import datetime
import asyncio
from appium_driver import AppiumDriver, SessionManager
from ai_engine import CommandParser, TestGenerator
from actions import ActionExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models
class ExecuteRequest(BaseModel):
    """Request model for executing natural language commands."""
    natural_language: str = Field(..., description="Natural language command")
    platform: str = Field("android", description="Platform: android or ios")
    device_id: Optional[str] = None
    capabilities: Optional[Dict[str, Any]] = None

class ExecuteResponse(BaseModel):
    """Response model for command execution."""
    status: str
    results: List[Dict[str, Any]]
    execution_time_ms: float
    screenshots: List[str] = []

class SessionRequest(BaseModel):
    """Request model for session creation."""
    platform: str
    device_id: Optional[str] = None
    capabilities: Optional[Dict[str, Any]] = None

class SessionResponse(BaseModel):
    """Response model for session creation."""
    session_id: str
    status: str
    timestamp: str

# Initialize FastAPI app
app = FastAPI(
    title="Appium MCP Server",
    description="AI-driven mobile automation MCP server",
    version="1.0.0"
)

# Global instances
session_manager = SessionManager()
command_parser = CommandParser()
action_executor = ActionExecutor()
test_generator = TestGenerator()

@app.on_event("startup")
async def startup_event():
    """Initialize server on startup."""
    logger.info("Appium MCP Server starting...")
    await session_manager.initialize()
    logger.info("Session manager initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Appium MCP Server...")
    await session_manager.cleanup()
    logger.info("Cleanup completed")

@app.post("/session/create", response_model=SessionResponse)
async def create_session(request: SessionRequest) -> SessionResponse:
    """Create a new Appium session."""
    try:
        logger.info(f"Creating session for {request.platform}")
        session_id = await session_manager.create_session(
            platform=request.platform,
            device_id=request.device_id,
            capabilities=request.capabilities
        )
        return SessionResponse(
            session_id=session_id,
            status="success",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Session creation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/session/{session_id}")
async def close_session(session_id: str):
    """Close an Appium session."""
    try:
        logger.info(f"Closing session: {session_id}")
        await session_manager.close_session(session_id)
        return {"status": "success", "message": f"Session {session_id} closed"}
    except Exception as e:
        logger.error(f"Session closure failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/execute", response_model=ExecuteResponse)
async def execute_command(request: ExecuteRequest) -> ExecuteResponse:
    """Execute natural language commands on mobile device."""
    start_time = datetime.now()
    screenshots = []
    
    try:
        logger.info(f"Processing command: {request.natural_language}")
        
        # Parse natural language to actions
        actions = command_parser.parse(request.natural_language)
        logger.info(f"Parsed {len(actions)} actions")
        
        # Get or create session
        if not request.device_id:
            request.device_id = "default"
        
        driver = await session_manager.get_driver(request.device_id)
        if not driver:
            driver = await session_manager.create_session(
                platform=request.platform,
                device_id=request.device_id,
                capabilities=request.capabilities
            )
        
        # Execute actions
        results = []
        for action in actions:
            result = await action_executor.execute(driver, action)
            results.append(result)
            
            # Capture screenshot if action contains screenshot command
            if action.get("type") == "screenshot":
                screenshot_path = await driver.save_screenshot()
                screenshots.append(screenshot_path)
        
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        logger.info(f"Command execution completed in {execution_time}ms")
        
        return ExecuteResponse(
            status="success",
            results=results,
            execution_time_ms=execution_time,
            screenshots=screenshots
        )
    
    except Exception as e:
        logger.error(f"Command execution failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-test")
async def generate_test(request: ExecuteRequest) -> Dict[str, Any]:
    """Generate pytest test from natural language scenario."""
    try:
        logger.info(f"Generating test for: {request.natural_language}")
        
        test_code = test_generator.generate_test(
            scenario=request.natural_language,
            platform=request.platform
        )
        
        return {
            "status": "success",
            "test_code": test_code,
            "language": "python",
            "framework": "pytest"
        }
    
    except Exception as e:
        logger.error(f"Test generation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/sessions")
async def list_sessions() -> Dict[str, Any]:
    """List all active sessions."""
    sessions = await session_manager.list_sessions()
    return {
        "status": "success",
        "count": len(sessions),
        "sessions": sessions
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)