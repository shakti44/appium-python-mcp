"""Session manager for Appium driver sessions."""
import uuid
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from appium import webdriver
from utils.logger import logger


class Session:
    """Represents an Appium session."""
    
    def __init__(
        self,
        session_id: str,
        driver: webdriver.Remote,
        capabilities: Dict[str, Any],
        created_at: Optional[datetime] = None
    ):
        """
        Initialize session.
        
        Args:
            session_id: Unique session identifier
            driver: Appium WebDriver instance
            capabilities: Session capabilities
            created_at: Session creation timestamp
        """
        self.session_id = session_id
        self.driver = driver
        self.capabilities = capabilities
        self.created_at = created_at or datetime.now()
        self.last_accessed = self.created_at
        self.metadata: Dict[str, Any] = {}
    
    def update_access_time(self):
        """Update last accessed timestamp."""
        self.last_accessed = datetime.now()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """
        Check if session is expired.
        
        Args:
            timeout_minutes: Timeout in minutes
            
        Returns:
            True if expired, False otherwise
        """
        expiration_time = self.last_accessed + timedelta(minutes=timeout_minutes)
        return datetime.now() > expiration_time
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get session information.
        
        Returns:
            Session info dictionary
        """
        return {
            "session_id": self.session_id,
            "capabilities": self.capabilities,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "metadata": self.metadata,
            "platform": self.capabilities.get("platformName", "Unknown"),
            "device": self.capabilities.get("deviceName", "Unknown")
        }


class SessionManager:
    """Manages Appium driver sessions."""
    
    def __init__(self, session_timeout_minutes: int = 30):
        """
        Initialize session manager.
        
        Args:
            session_timeout_minutes: Session timeout in minutes
        """
        self.sessions: Dict[str, Session] = {}
        self.session_timeout_minutes = session_timeout_minutes
        logger.info(f"SessionManager initialized with {session_timeout_minutes}min timeout")
    
    def create_session(
        self,
        server_url: str,
        capabilities: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> str:
        """
        Create a new Appium session.
        
        Args:
            server_url: Appium server URL
            capabilities: Desired capabilities
            session_id: Optional custom session ID
            
        Returns:
            Session ID
        """
        session_id = session_id or str(uuid.uuid4())
        
        try:
            logger.info(f"Creating session {session_id} with capabilities: {capabilities}")
            driver = webdriver.Remote(server_url, options=self._build_options(capabilities))
            
            session = Session(
                session_id=session_id,
                driver=driver,
                capabilities=capabilities
            )
            
            self.sessions[session_id] = session
            logger.info(f"Session {session_id} created successfully")
            
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create session {session_id}: {e}")
            raise
    
    def _build_options(self, capabilities: Dict[str, Any]) -> Any:
        """
        Build Appium options from capabilities.
        
        Args:
            capabilities: Capabilities dictionary
            
        Returns:
            Appium options object
        """
        # This is a simplified version - in production you'd use proper UiAutomator2Options, XCUITestOptions
        from selenium.webdriver.common.options import BaseOptions
        
        class AppiumOptions(BaseOptions):
            def __init__(self):
                super().__init__()
                self._caps = {}
            
            @property
            def capabilities(self):
                return self._caps
            
            def set_capability(self, name, value):
                self._caps[name] = value
        
        options = AppiumOptions()
        for key, value in capabilities.items():
            options.set_capability(key, value)
        
        return options
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session object or None
        """
        session = self.sessions.get(session_id)
        if session:
            session.update_access_time()
        return session
    
    def get_driver(self, session_id: str) -> Optional[webdriver.Remote]:
        """
        Get driver for session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            WebDriver instance or None
        """
        session = self.get_session(session_id)
        return session.driver if session else None
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete session and quit driver.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        session = self.sessions.get(session_id)
        if not session:
            logger.warning(f"Session {session_id} not found for deletion")
            return False
        
        try:
            logger.info(f"Deleting session {session_id}")
            session.driver.quit()
            del self.sessions[session_id]
            logger.info(f"Session {session_id} deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            # Still remove from sessions dict even if quit fails
            self.sessions.pop(session_id, None)
            return False
    
    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        List all active sessions.
        
        Returns:
            Dictionary of session IDs to session info
        """
        return {
            sid: session.get_info()
            for sid, session in self.sessions.items()
        }
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions."""
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if session.is_expired(self.session_timeout_minutes)
        ]
        
        for sid in expired_sessions:
            logger.info(f"Cleaning up expired session: {sid}")
            self.delete_session(sid)
    
    def delete_all_sessions(self):
        """Delete all active sessions."""
        session_ids = list(self.sessions.keys())
        for sid in session_ids:
            self.delete_session(sid)
        logger.info("All sessions deleted")
