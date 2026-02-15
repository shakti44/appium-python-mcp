"""FastAPI-based MCP Server for Appium

This is the main MCP server that handles session management, device commands,
and Appium automation requests.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import sys
import os

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.session_manager import SessionManager
from src.device_handler import list_devices, send_command, get_device_status
from appium_driver.driver import AppiumDriver

app = FastAPI(
    title="Appium MCP Server",
    description="MCP Server for Appium mobile automation",
    version="0.1.0"
)

# Initialize session manager
session_manager = SessionManager()

# Store active drivers
active_drivers: Dict[str, AppiumDriver] = {}


# Request/Response Models
class SessionCreateRequest(BaseModel):
    platform_name: str
    device_name: str
    app: str
    automation_name: str = 'UiAutomator2'
    appium_server_url: str = 'http://localhost:4723'


class SessionCreateResponse(BaseModel):
    session_id: str
    status: str


class CommandRequest(BaseModel):
    session_id: str
    command: str
    parameters: Dict[str, Any] = {}


class CommandResponse(BaseModel):
    session_id: str
    command: str
    status: str
    result: Any


class DeviceCommandRequest(BaseModel):
    device_id: str
    command: str


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "running",
        "service": "Appium MCP Server",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Session Management Endpoints
@app.post("/session/", response_model=SessionCreateResponse)
async def create_session(request: SessionCreateRequest):
    """Create a new Appium session"""
    try:
        # Create session in session manager
        session_id = session_manager.create_session(
            data={
                'platform_name': request.platform_name,
                'device_name': request.device_name,
                'app': request.app,
                'automation_name': request.automation_name,
                'appium_server_url': request.appium_server_url
            }
        )
        
        # Initialize Appium driver
        driver = AppiumDriver(
            platform_name=request.platform_name,
            device_name=request.device_name,
            app=request.app,
            automation_name=request.automation_name,
            appium_server_url=request.appium_server_url
        )
        
        # Store driver
        active_drivers[session_id] = driver
        
        return SessionCreateResponse(
            session_id=session_id,
            status="created"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session details"""
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    # Quit driver if exists
    if session_id in active_drivers:
        try:
            active_drivers[session_id].quit()
        except Exception:
            pass  # Ignore errors when quitting
        del active_drivers[session_id]
    
    # Delete from session manager
    if session_manager.delete_session(session_id):
        return {"session_id": session_id, "status": "deleted"}
    raise HTTPException(status_code=404, detail="Session not found")


@app.get("/sessions/")
async def list_sessions():
    """List all active sessions"""
    session_ids = session_manager.list_sessions()
    sessions = []
    for session_id in session_ids:
        session = session_manager.get_session(session_id)
        if session:
            sessions.append(session)
    return {"sessions": sessions, "count": len(sessions)}


# Command Processing Endpoints
@app.post("/command/", response_model=CommandResponse)
async def process_command(cmd: CommandRequest):
    """Process an Appium command"""
    session_id = cmd.session_id
    command = cmd.command
    parameters = cmd.parameters
    
    # Check if session is active
    if not session_manager.is_session_active(session_id):
        raise HTTPException(status_code=404, detail="Session not found or inactive")
    
    # Get driver
    driver = active_drivers.get(session_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found for session")
    
    try:
        # Process commands
        result = None
        
        if command == "start":
            result = driver.start()
            result = "Driver started successfully"
            
        elif command == "quit":
            driver.quit()
            result = "Driver quit successfully"
            
        elif command == "find_element":
            by = parameters.get("by")
            value = parameters.get("value")
            element = driver.find_element(by, value)
            result = {"element_id": element.id if hasattr(element, 'id') else str(element)}
            
        elif command == "tap":
            x = parameters.get("x")
            y = parameters.get("y")
            driver.tap(x, y)
            result = f"Tapped at ({x}, {y})"
            
        elif command == "swipe":
            start_x = parameters.get("start_x")
            start_y = parameters.get("start_y")
            end_x = parameters.get("end_x")
            end_y = parameters.get("end_y")
            duration = parameters.get("duration", 1000)
            driver.swipe(start_x, start_y, end_x, end_y, duration)
            result = f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})"
            
        elif command == "get_page_source":
            result = driver.get_page_source()
            
        elif command == "screenshot":
            filename = parameters.get("filename", "screenshot.png")
            driver.screenshot(filename)
            result = f"Screenshot saved to {filename}"
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown command: {command}")
        
        return CommandResponse(
            session_id=session_id,
            command=command,
            status="success",
            result=result
        )
        
    except Exception as e:
        return CommandResponse(
            session_id=session_id,
            command=command,
            status="error",
            result=str(e)
        )


# Device Management Endpoints
@app.get("/devices/")
async def get_devices():
    """List all connected devices"""
    devices = list_devices()
    return {"devices": devices, "count": len(devices)}


@app.get("/device/{device_id}")
async def get_device(device_id: str):
    """Get device status"""
    status = get_device_status(device_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return status


@app.post("/device/command/")
async def send_device_command(request: DeviceCommandRequest):
    """Send a command to a device"""
    result = send_command(request.device_id, request.command)
    if not result.get('success', False):
        raise HTTPException(status_code=500, detail=result.get('error', 'Command failed'))
    return result


# Server Management
@app.post("/server/cleanup")
async def cleanup_sessions():
    """Cleanup expired sessions"""
    count = session_manager.cleanup_expired_sessions()
    return {"cleaned_sessions": count}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
