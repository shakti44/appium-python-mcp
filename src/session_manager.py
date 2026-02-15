"""Session Manager

This module manages sessions for the Appium MCP server.
"""

import uuid
import time
from typing import Dict, Any, Optional, List


class SessionManager:
    """Manages Appium sessions with expiration support"""
    
    def __init__(self, default_timeout: int = 3600):
        """Initialize SessionManager
        
        Args:
            default_timeout: Default session timeout in seconds (default: 1 hour)
        """
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.default_timeout = default_timeout

    def create_session(self, session_id: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> str:
        """Creates a new session
        
        Args:
            session_id: Optional session ID. If not provided, a UUID will be generated.
            data: Optional session data
            
        Returns:
            The session ID
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        session_data = data if data is not None else {}
        session_data.update({
            'id': session_id,
            'created_at': time.time(),
            'last_activity': time.time(),
            'expires_at': time.time() + self.default_timeout,
            'active': True
        })
        
        self.sessions[session_id] = session_data
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves session data by session_id
        
        Args:
            session_id: The session identifier
            
        Returns:
            Session data or None if not found
        """
        session = self.sessions.get(session_id)
        if session and session.get('active', False):
            # Update last activity
            session['last_activity'] = time.time()
        return session

    def delete_session(self, session_id: str) -> bool:
        """Deletes the session with the given session_id
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if session was deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def list_sessions(self) -> List[str]:
        """Returns a list of all active session IDs
        
        Returns:
            List of active session IDs
        """
        return [sid for sid, session in self.sessions.items() if session.get('active', False)]
    
    def expire_session(self, session_id: str) -> bool:
        """Expires a session by marking it as inactive
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if session was expired, False if not found
        """
        if session_id in self.sessions:
            self.sessions[session_id]['active'] = False
            self.sessions[session_id]['expires_at'] = time.time()
            return True
        return False
    
    def is_session_active(self, session_id: str) -> bool:
        """Check if a session is active
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if session exists and is active, False otherwise
        """
        session = self.sessions.get(session_id)
        if session is None:
            return False
        
        # Check if session is marked as active and hasn't expired
        if not session.get('active', False):
            return False
        
        if time.time() > session.get('expires_at', 0):
            # Session has expired, mark it inactive
            session['active'] = False
            return False
        
        return True
    
    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions
        
        Returns:
            Number of sessions removed
        """
        current_time = time.time()
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if current_time > session.get('expires_at', 0)
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        return len(expired_sessions)
