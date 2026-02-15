import unittest
import sys
import os

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.session_manager import SessionManager


class TestSessionManager(unittest.TestCase):

    def setUp(self):
        self.session_manager = SessionManager()

    def test_create_session(self):
        session_id = self.session_manager.create_session()
        self.assertIsNotNone(session_id)

    def test_get_session(self):
        session_id = self.session_manager.create_session()
        session = self.session_manager.get_session(session_id)
        self.assertIsNotNone(session)
        self.assertEqual(session['id'], session_id)

    def test_delete_session(self):
        session_id = self.session_manager.create_session()
        self.session_manager.delete_session(session_id)
        session = self.session_manager.get_session(session_id)
        self.assertIsNone(session)

    def test_session_expiration(self):
        session_id = self.session_manager.create_session()
        self.session_manager.expire_session(session_id)
        self.assertFalse(self.session_manager.is_session_active(session_id))


if __name__ == '__main__':
    unittest.main()