"""Pydantic schemas for MCP server requests and responses."""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class SessionCreateRequest(BaseModel):
    """Request to create a new session."""
    platform: str = Field(..., description="Platform name (Android/iOS)")
    capabilities: Dict[str, Any] = Field(default_factory=dict, description="Custom capabilities")
    session_id: Optional[str] = Field(None, description="Optional custom session ID")


class SessionCreateResponse(BaseModel):
    """Response from session creation."""
    session_id: str
    status: str
    message: str


class SessionInfo(BaseModel):
    """Session information."""
    session_id: str
    capabilities: Dict[str, Any]
    created_at: str
    last_accessed: str
    platform: str
    device: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CommandRequest(BaseModel):
    """Request to execute a command."""
    session_id: str
    command: str = Field(..., description="Natural language command or action name")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Command parameters")


class CommandResponse(BaseModel):
    """Response from command execution."""
    session_id: str
    command: str
    status: str
    result: Any = None
    error: Optional[str] = None
    screenshot_path: Optional[str] = None
    execution_time: float


class ElementFindRequest(BaseModel):
    """Request to find an element."""
    session_id: str
    strategy: str = Field(..., description="Locator strategy")
    value: str = Field(..., description="Locator value")
    timeout: Optional[int] = Field(None, description="Custom timeout in seconds")


class ElementActionRequest(BaseModel):
    """Request to perform element action."""
    session_id: str
    action: str = Field(..., description="Action name (click, type, etc.)")
    target: str = Field(..., description="Element target")
    value: Optional[str] = Field(None, description="Value for actions like type")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)


class GestureRequest(BaseModel):
    """Request to perform gesture."""
    session_id: str
    gesture: str = Field(..., description="Gesture type (swipe, tap, etc.)")
    params: Dict[str, Any] = Field(default_factory=dict, description="Gesture parameters")


class TestGenerationRequest(BaseModel):
    """Request to generate test code."""
    test_name: str
    commands: List[str] = Field(..., description="List of natural language commands")
    description: Optional[str] = None
    platform: str = "Android"


class TestGenerationResponse(BaseModel):
    """Response with generated test code."""
    test_name: str
    test_code: str
    message: str


class PageObjectGenerationRequest(BaseModel):
    """Request to generate page object."""
    page_name: str
    elements: List[Dict[str, str]] = Field(..., description="Element definitions")
    platform: str = "Android"


class PageObjectGenerationResponse(BaseModel):
    """Response with generated page object code."""
    page_name: str
    page_code: str
    message: str


class ScreenshotRequest(BaseModel):
    """Request to take screenshot."""
    session_id: str
    name: Optional[str] = None


class ScreenshotResponse(BaseModel):
    """Response with screenshot path."""
    session_id: str
    screenshot_path: str
    timestamp: str


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: str
    active_sessions: int


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    message: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None
