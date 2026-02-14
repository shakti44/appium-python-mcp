"""Request handlers for MCP server."""
import time
from typing import Dict, Any, Optional
from datetime import datetime
from appium_driver.session_manager import SessionManager
from appium_driver.driver import AppiumDriverWrapper
from appium_driver.capabilities import create_android_capabilities, create_ios_capabilities
from ai_engine.nlp_processor import NLPProcessor, ParsedCommand
from ai_engine.command_parser import CommandParser
from ai_engine.test_generator import TestGenerator
from config.environment import settings, config_manager
from utils.logger import logger
from mcp_server.schemas import *


class MCPHandlers:
    """Handlers for MCP server requests."""
    
    def __init__(self):
        """Initialize MCP handlers."""
        self.session_manager = SessionManager()
        self.nlp_processor = NLPProcessor()
        self.test_generator = TestGenerator()
        self.logger = logger
        
        # Cache for command parsers by session
        self._parsers: Dict[str, CommandParser] = {}
    
    def _get_command_parser(self, session_id: str) -> CommandParser:
        """Get or create command parser for session."""
        if session_id not in self._parsers:
            session = self.session_manager.get_session(session_id)
            if not session:
                raise ValueError(f"Session not found: {session_id}")
            
            driver_wrapper = AppiumDriverWrapper(session.driver)
            self._parsers[session_id] = CommandParser(driver_wrapper)
        
        return self._parsers[session_id]
    
    async def create_session(self, request: SessionCreateRequest) -> SessionCreateResponse:
        """
        Create a new Appium session.
        
        Args:
            request: Session creation request
            
        Returns:
            SessionCreateResponse
        """
        try:
            self.logger.info(f"Creating session for platform: {request.platform}")
            
            # Load base capabilities
            base_caps = config_manager.load_capabilities(request.platform)
            
            # Merge with custom capabilities
            capabilities = config_manager.merge_capabilities(base_caps, request.capabilities)
            
            # Create session
            session_id = self.session_manager.create_session(
                server_url=settings.appium_server_url,
                capabilities=capabilities,
                session_id=request.session_id
            )
            
            return SessionCreateResponse(
                session_id=session_id,
                status="success",
                message=f"Session created successfully for {request.platform}"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create session: {e}")
            raise
    
    async def delete_session(self, session_id: str) -> Dict[str, Any]:
        """
        Delete a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Response dictionary
        """
        try:
            # Remove parser cache
            self._parsers.pop(session_id, None)
            
            success = self.session_manager.delete_session(session_id)
            
            if success:
                return {
                    "session_id": session_id,
                    "status": "success",
                    "message": "Session deleted successfully"
                }
            else:
                return {
                    "session_id": session_id,
                    "status": "not_found",
                    "message": "Session not found"
                }
                
        except Exception as e:
            self.logger.error(f"Failed to delete session: {e}")
            raise
    
    async def get_session(self, session_id: str) -> SessionInfo:
        """
        Get session information.
        
        Args:
            session_id: Session identifier
            
        Returns:
            SessionInfo
        """
        session = self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        info = session.get_info()
        return SessionInfo(**info)
    
    async def list_sessions(self) -> Dict[str, SessionInfo]:
        """
        List all active sessions.
        
        Returns:
            Dictionary of session IDs to SessionInfo
        """
        sessions = self.session_manager.list_sessions()
        return {
            sid: SessionInfo(**info)
            for sid, info in sessions.items()
        }
    
    async def execute_command(self, request: CommandRequest) -> CommandResponse:
        """
        Execute a natural language command.
        
        Args:
            request: Command request
            
        Returns:
            CommandResponse
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Executing command: {request.command}")
            
            # Parse natural language command
            parsed = self.nlp_processor.parse_command(request.command)
            
            # Override with explicit params if provided
            if request.params:
                parsed.params.update(request.params)
            
            # Get command parser
            parser = self._get_command_parser(request.session_id)
            
            # Execute command
            result = parser.execute_command(parsed)
            
            execution_time = time.time() - start_time
            
            return CommandResponse(
                session_id=request.session_id,
                command=request.command,
                status="success",
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            execution_time = time.time() - start_time
            
            return CommandResponse(
                session_id=request.session_id,
                command=request.command,
                status="error",
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute_element_action(self, request: ElementActionRequest) -> CommandResponse:
        """
        Execute an element action.
        
        Args:
            request: Element action request
            
        Returns:
            CommandResponse
        """
        # Convert to command format
        command_text = f"{request.action} on {request.target}"
        if request.value:
            command_text += f" with '{request.value}'"
        
        command_request = CommandRequest(
            session_id=request.session_id,
            command=command_text,
            params=request.params
        )
        
        return await self.execute_command(command_request)
    
    async def execute_gesture(self, request: GestureRequest) -> CommandResponse:
        """
        Execute a gesture.
        
        Args:
            request: Gesture request
            
        Returns:
            CommandResponse
        """
        start_time = time.time()
        
        try:
            session = self.session_manager.get_session(request.session_id)
            if not session:
                raise ValueError(f"Session not found: {request.session_id}")
            
            driver_wrapper = AppiumDriverWrapper(session.driver)
            
            # Import gesture actions
            from actions.gesture_actions import GestureActions
            gesture_actions = GestureActions(driver_wrapper)
            
            # Execute gesture
            result = gesture_actions.execute_action(request.gesture, **request.params)
            
            execution_time = time.time() - start_time
            
            return CommandResponse(
                session_id=request.session_id,
                command=f"gesture: {request.gesture}",
                status="success",
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Gesture execution failed: {e}")
            execution_time = time.time() - start_time
            
            return CommandResponse(
                session_id=request.session_id,
                command=f"gesture: {request.gesture}",
                status="error",
                error=str(e),
                execution_time=execution_time
            )
    
    async def take_screenshot(self, request: ScreenshotRequest) -> ScreenshotResponse:
        """
        Take a screenshot.
        
        Args:
            request: Screenshot request
            
        Returns:
            ScreenshotResponse
        """
        session = self.session_manager.get_session(request.session_id)
        if not session:
            raise ValueError(f"Session not found: {request.session_id}")
        
        driver_wrapper = AppiumDriverWrapper(session.driver)
        screenshot_path = driver_wrapper.take_screenshot(request.name)
        
        return ScreenshotResponse(
            session_id=request.session_id,
            screenshot_path=str(screenshot_path),
            timestamp=datetime.now().isoformat()
        )
    
    async def generate_test(self, request: TestGenerationRequest) -> TestGenerationResponse:
        """
        Generate test code from commands.
        
        Args:
            request: Test generation request
            
        Returns:
            TestGenerationResponse
        """
        # Parse commands
        parsed_commands = []
        for cmd_text in request.commands:
            parsed = self.nlp_processor.parse_command(cmd_text)
            parsed_commands.append(parsed)
        
        # Generate test code
        test_code = self.test_generator.generate_test_from_commands(
            test_name=request.test_name,
            commands=parsed_commands,
            description=request.description,
            platform=request.platform
        )
        
        return TestGenerationResponse(
            test_name=request.test_name,
            test_code=test_code,
            message="Test code generated successfully"
        )
    
    async def generate_page_object(
        self,
        request: PageObjectGenerationRequest
    ) -> PageObjectGenerationResponse:
        """
        Generate page object code.
        
        Args:
            request: Page object generation request
            
        Returns:
            PageObjectGenerationResponse
        """
        page_code = self.test_generator.generate_page_object(
            page_name=request.page_name,
            elements=request.elements,
            platform=request.platform
        )
        
        return PageObjectGenerationResponse(
            page_name=request.page_name,
            page_code=page_code,
            message="Page object code generated successfully"
        )
    
    async def health_check(self) -> HealthCheckResponse:
        """
        Perform health check.
        
        Returns:
            HealthCheckResponse
        """
        active_sessions = len(self.session_manager.sessions)
        
        return HealthCheckResponse(
            status="healthy",
            version="1.0.0",
            timestamp=datetime.now().isoformat(),
            active_sessions=active_sessions
        )
