class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id, data):
        """Creates a new session with the given session_id and data."""
        self.sessions[session_id] = data

    def get_session(self, session_id):
        """Retrieves session data by session_id."""
        return self.sessions.get(session_id, None)

    def delete_session(self, session_id):
        """Deletes the session with the given session_id."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self):
        """Returns a list of all active sessions."""
        return self.sessions.keys()