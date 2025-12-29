import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from auth_system import AuthSystem


class TestAuthSystem(unittest.TestCase):
    """Comprehensive tests for AuthSystem class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.auth = AuthSystem()
    
    def tearDown(self):
        """Clean up after tests"""
        self.auth = None
    
    # Test __init__
    def test_init_creates_empty_sessions(self):
        """Test that initialization creates empty sessions dictionary"""
        self.assertEqual(self.auth.sessions, {})
        self.assertIsInstance(self.auth.sessions, dict)
    
    def test_init_creates_empty_failed_attempts(self):
        """Test that initialization creates empty failed_attempts dictionary"""
        self.assertEqual(self.auth.failed_attempts, {})
        self.assertIsInstance(self.auth.failed_attempts, dict)
    
    # Test login - successful cases
    def test_login_successful_with_valid_credentials(self):
        """Test successful login with correct credentials"""
        result = self.auth.login("admin", "admin123")
        self.assertEqual(result, "session_admin_12345")
        self.assertIn("session_admin_12345", self.auth.sessions)
        self.assertEqual(self.auth.sessions["session_admin_12345"], "admin")
    
    def test_login_successful_resets_failed_attempts(self):
        """Test that successful login resets failed attempts to 0"""
        self.auth.failed_attempts["admin"] = 3
        self.auth.login("admin", "admin123")
        self.assertEqual(self.auth.failed_attempts["admin"], 0)
    
    def test_login_successful_creates_session_token(self):
        """Test that successful login creates expected session token"""
        token = self.auth.login("admin", "admin123")
        self.assertTrue(token.startswith("session_"))
        self.assertIn("admin", token)
    
    # Test login - failed attempts tracking
    def test_login_failed_increments_attempt_counter(self):
        """Test that failed login increments attempt counter"""
        self.auth.login("admin", "wrongpass")
        self.assertEqual(self.auth.failed_attempts["admin"], 1)
    
    def test_login_failed_multiple_attempts_increments(self):
        """Test multiple failed attempts increment correctly"""
        self.auth.login("admin", "wrong1")
        self.auth.login("admin", "wrong2")
        self.auth.login("admin", "wrong3")
        self.assertEqual(self.auth.failed_attempts["admin"], 3)
    
    def test_login_failed_initializes_attempts_for_new_user(self):
        """Test that failed attempts are initialized for new username"""
        self.auth.login("newuser", "wrongpass")
        self.assertIn("newuser", self.auth.failed_attempts)
        self.assertEqual(self.auth.failed_attempts["newuser"], 1)
    
    def test_login_failed_returns_none(self):
        """Test that failed login returns None"""
        result = self.auth.login("admin", "wrongpass")
        self.assertIsNone(result)
    
    # Test login - account lockout after 5 attempts
    @patch('smtplib.SMTP')
    def test_login_locks_account_after_5_failures(self, mock_smtp):
        """Test that account locks after 5 failed attempts"""
        # Set up mock
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Fail 5 times
        for i in range(5):
            self.auth.login("admin", "wrongpass")
        
        # 6th attempt should return ACCOUNT_LOCKED
        result = self.auth.login("admin", "admin123")
        self.assertEqual(result, "ACCOUNT_LOCKED")
    
    @patch('smtplib.SMTP')
    def test_login_sends_email_on_5th_failure(self, mock_smtp):
        """Test that email is sent on 5th failed attempt"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Fail 5 times
        for i in range(5):
            self.auth.login("admin", "wrongpass")
        
        # Verify email was sent
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called()
        mock_server.login.assert_called_with("admin@shop.com", "password123")
        mock_server.sendmail.assert_called()
        mock_server.quit.assert_called()
    
    @patch('smtplib.SMTP')
    def test_login_email_contains_username_in_message(self, mock_smtp):
        """Test that alert email contains the locked username"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        for i in range(5):
            self.auth.login("testuser", "wrongpass")
        
        # Check the message contains username
        call_args = mock_server.sendmail.call_args[0]
        message = call_args[2]
        self.assertIn("testuser", message)
        self.assertIn("Account locked", message)
    
    @patch('smtplib.SMTP')
    def test_login_account_locked_prevents_further_attempts(self, mock_smtp):
        """Test that locked account prevents all further login attempts"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Lock the account
        for i in range(5):
            self.auth.login("admin", "wrongpass")
        
        # Try with correct password - should still be locked
        result = self.auth.login("admin", "admin123")
        self.assertEqual(result, "ACCOUNT_LOCKED")
        self.assertNotIn("session_admin_12345", self.auth.sessions)
    
    # Test login - edge cases with empty/None inputs
    def test_login_with_empty_username_returns_none(self):
        """Test login with empty username returns None"""
        result = self.auth.login("", "admin123")
        self.assertIsNone(result)
    
    def test_login_with_none_username_returns_none(self):
        """Test login with None username returns None"""
        result = self.auth.login(None, "admin123")
        self.assertIsNone(result)
    
    def test_login_with_empty_password_returns_none(self):
        """Test login with empty password returns None"""
        result = self.auth.login("admin", "")
        self.assertIsNone(result)
    
    def test_login_with_none_password_returns_none(self):
        """Test login with None password returns None"""
        result = self.auth.login("admin", None)
        self.assertIsNone(result)
    
    def test_login_with_both_empty_returns_none(self):
        """Test login with both username and password empty returns None"""
        result = self.auth.login("", "")
        self.assertIsNone(result)
    
    def test_login_with_both_none_returns_none(self):
        """Test login with both username and password None returns None"""
        result = self.auth.login(None, None)
        self.assertIsNone(result)
    
    # Test login - failed attempts initialization path
    def test_login_initializes_failed_attempts_to_zero(self):
        """Test that new user's failed attempts start at 0"""
        self.auth.login("newuser", "wrongpass")
        # After first failure, should be 1
        self.assertEqual(self.auth.failed_attempts["newuser"], 1)
    
    def test_login_does_not_reinitialize_existing_attempts(self):
        """Test that existing failed attempts are not reinitialized"""
        self.auth.failed_attempts["admin"] = 2
        self.auth.login("admin", "wrongpass")
        self.assertEqual(self.auth.failed_attempts["admin"], 3)
    
    # Test logout - successful cases
    def test_logout_with_valid_token_returns_true(self):
        """Test logout with valid session token returns True"""
        token = self.auth.login("admin", "admin123")
        result = self.auth.logout(token)
        self.assertTrue(result)
    
    def test_logout_removes_session_from_sessions_dict(self):
        """Test that logout removes session from sessions dictionary"""
        token = self.auth.login("admin", "admin123")
        self.auth.logout(token)
        self.assertNotIn(token, self.auth.sessions)
    
    def test_logout_with_invalid_token_returns_false(self):
        """Test logout with invalid token returns False"""
        result = self.auth.logout("invalid_token")
        self.assertFalse(result)
    
    def test_logout_with_empty_token_returns_false(self):
        """Test logout with empty token returns False"""
        result = self.auth.logout("")
        self.assertFalse(result)
    
    def test_logout_with_none_token_returns_false(self):
        """Test logout with None token returns False"""
        result = self.auth.logout(None)
        self.assertFalse(result)
    
    def test_logout_already_logged_out_token_returns_false(self):
        """Test logout with already logged out token returns False"""
        token = self.auth.login("admin", "admin123")
        self.auth.logout(token)
        result = self.auth.logout(token)
        self.assertFalse(result)
    
    # Test multiple sessions
    def test_multiple_sessions_can_coexist(self):
        """Test that multiple sessions can exist simultaneously"""
        token1 = self.auth.login("admin", "admin123")
        auth2 = AuthSystem()
        token2 = auth2.login("admin", "admin123")
        
        self.assertIn(token1, self.auth.sessions)
        self.assertIn(token2, auth2.sessions)
    
    def test_logout_only_affects_specific_session(self):
        """Test that logout only removes the specific session"""
        self.auth.sessions["token1"] = "user1"
        self.auth.sessions["token2"] = "user2"
        
        self.auth.logout("token1")
        
        self.assertNotIn("token1", self.auth.sessions)
        self.assertIn("token2", self.auth.sessions)


if __name__ == '__main__':
    unittest.main()
