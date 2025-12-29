import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from user_manager import UserManager


class TestUserManager(unittest.TestCase):
    """Comprehensive tests for UserManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = UserManager()
    
    def tearDown(self):
        """Clean up after tests"""
        self.manager = None
    
    # Test __init__
    def test_init_creates_empty_users_list(self):
        """Test that initialization creates empty users list"""
        self.assertEqual(self.manager.users, [])
        self.assertIsInstance(self.manager.users, list)
    
    def test_init_sets_db_connection(self):
        """Test that initialization sets database connection string"""
        self.assertEqual(self.manager.db_connection, "mysql://localhost/ecommerce")
    
    def test_init_creates_email_service(self):
        """Test that initialization creates email service instance"""
        self.assertIsNotNone(self.manager.email_service)
    
    # Test create_user - successful customer creation
    @patch('email_mock.MockEmailService.send_email')
    def test_create_customer_with_valid_data_returns_true(self, mock_send):
        """Test creating customer with valid data returns True"""
        result = self.manager.create_user("john_doe", "john@email.com", "password123", "customer")
        self.assertTrue(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_customer_adds_to_users_list(self, mock_send):
        """Test creating customer adds user to users list"""
        self.manager.create_user("john_doe", "john@email.com", "password123", "customer")
        self.assertEqual(len(self.manager.users), 1)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_customer_has_correct_fields(self, mock_send):
        """Test created customer has correct fields"""
        self.manager.create_user("john_doe", "john@email.com", "password123", "customer")
        user = self.manager.users[0]
        
        self.assertEqual(user["username"], "john_doe")
        self.assertEqual(user["email"], "john@email.com")
        self.assertEqual(user["password"], "password123")
        self.assertEqual(user["type"], "customer")
        self.assertEqual(user["discount"], 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_customer_sends_welcome_email(self, mock_send):
        """Test creating customer sends welcome email"""
        self.manager.create_user("john_doe", "john@email.com", "password123", "customer")
        
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0]
        self.assertEqual(call_args[0], "admin@shop.com")
        self.assertEqual(call_args[1], "john@email.com")
        self.assertIn("Welcome john_doe!", call_args[2])
    
    # Test create_user - successful premium creation
    @patch('email_mock.MockEmailService.send_email')
    def test_create_premium_with_valid_data_returns_true(self, mock_send):
        """Test creating premium user with valid data returns True"""
        result = self.manager.create_user("premium_user", "premium@email.com", "securepass", "premium")
        self.assertTrue(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_premium_has_correct_discount(self, mock_send):
        """Test created premium user has 10% discount"""
        self.manager.create_user("premium_user", "premium@email.com", "securepass", "premium")
        user = self.manager.users[0]
        
        self.assertEqual(user["type"], "premium")
        self.assertEqual(user["discount"], 10)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_premium_sends_welcome_email(self, mock_send):
        """Test creating premium user sends welcome email"""
        self.manager.create_user("premium_user", "premium@email.com", "securepass", "premium")
        
        call_args = mock_send.call_args[0]
        self.assertIn("Welcome Premium premium_user!", call_args[2])
    
    # Test create_user - successful VIP creation
    @patch('email_mock.MockEmailService.send_email')
    def test_create_vip_with_valid_data_returns_true(self, mock_send):
        """Test creating VIP user with valid data returns True"""
        result = self.manager.create_user("vip_user", "vip@email.com", "vippassword", "vip")
        self.assertTrue(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_vip_has_correct_discount(self, mock_send):
        """Test created VIP user has 20% discount"""
        self.manager.create_user("vip_user", "vip@email.com", "vippassword", "vip")
        user = self.manager.users[0]
        
        self.assertEqual(user["type"], "vip")
        self.assertEqual(user["discount"], 20)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_vip_sends_welcome_email(self, mock_send):
        """Test creating VIP user sends welcome email"""
        self.manager.create_user("vip_user", "vip@email.com", "vippassword", "vip")
        
        call_args = mock_send.call_args[0]
        self.assertIn("Welcome VIP vip_user!", call_args[2])
    
    # Test create_user - validation failures
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_empty_username_returns_false(self, mock_send):
        """Test creating user with empty username returns False"""
        result = self.manager.create_user("", "email@test.com", "password123", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_none_username_returns_false(self, mock_send):
        """Test creating user with None username returns False"""
        result = self.manager.create_user(None, "email@test.com", "password123", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_empty_email_returns_false(self, mock_send):
        """Test creating user with empty email returns False"""
        result = self.manager.create_user("username", "", "password123", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_none_email_returns_false(self, mock_send):
        """Test creating user with None email returns False"""
        result = self.manager.create_user("username", None, "password123", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_empty_password_returns_false(self, mock_send):
        """Test creating user with empty password returns False"""
        result = self.manager.create_user("username", "email@test.com", "", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_none_password_returns_false(self, mock_send):
        """Test creating user with None password returns False"""
        result = self.manager.create_user("username", "email@test.com", None, "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_short_password_returns_false(self, mock_send):
        """Test creating user with password < 8 chars returns False"""
        result = self.manager.create_user("username", "email@test.com", "pass", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_password_exactly_8_chars_succeeds(self, mock_send):
        """Test creating user with password exactly 8 chars succeeds"""
        result = self.manager.create_user("username", "email@test.com", "password", "customer")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.users), 1)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_password_7_chars_fails(self, mock_send):
        """Test creating user with password 7 chars fails"""
        result = self.manager.create_user("username", "email@test.com", "passwor", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_email_without_at_returns_false(self, mock_send):
        """Test creating user with email without @ returns False"""
        result = self.manager.create_user("username", "invalidemail.com", "password123", "customer")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_email_with_at_succeeds(self, mock_send):
        """Test creating user with email containing @ succeeds"""
        result = self.manager.create_user("username", "valid@email.com", "password123", "customer")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.users), 1)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_create_user_invalid_user_type_returns_false(self, mock_send):
        """Test creating user with invalid user type returns False"""
        result = self.manager.create_user("username", "email@test.com", "password123", "invalid")
        self.assertFalse(result)
        self.assertEqual(len(self.manager.users), 0)
    
    # Test multiple user creation
    @patch('email_mock.MockEmailService.send_email')
    def test_create_multiple_users(self, mock_send):
        """Test creating multiple users"""
        self.manager.create_user("user1", "user1@test.com", "password123", "customer")
        self.manager.create_user("user2", "user2@test.com", "password123", "premium")
        self.manager.create_user("user3", "user3@test.com", "password123", "vip")
        
        self.assertEqual(len(self.manager.users), 3)
    
    # Test validate_user - successful validation
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_correct_credentials_returns_true(self, mock_send):
        """Test validating user with correct credentials returns True"""
        self.manager.create_user("john", "john@test.com", "password123", "customer")
        result = self.manager.validate_user("john", "password123")
        self.assertTrue(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_wrong_password_returns_false(self, mock_send):
        """Test validating user with wrong password returns False"""
        self.manager.create_user("john", "john@test.com", "password123", "customer")
        result = self.manager.validate_user("john", "wrongpassword")
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_nonexistent_username_returns_false(self, mock_send):
        """Test validating non-existent username returns False"""
        result = self.manager.validate_user("nonexistent", "password123")
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_empty_username_returns_false(self, mock_send):
        """Test validating with empty username returns False"""
        result = self.manager.validate_user("", "password123")
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_none_username_returns_false(self, mock_send):
        """Test validating with None username returns False"""
        result = self.manager.validate_user(None, "password123")
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_empty_password_returns_false(self, mock_send):
        """Test validating with empty password returns False"""
        result = self.manager.validate_user("john", "")
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_none_password_returns_false(self, mock_send):
        """Test validating with None password returns False"""
        result = self.manager.validate_user("john", None)
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_both_empty_returns_false(self, mock_send):
        """Test validating with both empty returns False"""
        result = self.manager.validate_user("", "")
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_both_none_returns_false(self, mock_send):
        """Test validating with both None returns False"""
        result = self.manager.validate_user(None, None)
        self.assertFalse(result)
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_case_sensitive_username(self, mock_send):
        """Test validating user with different case username"""
        self.manager.create_user("john", "john@test.com", "password123", "customer")
        result = self.manager.validate_user("John", "password123")
        self.assertFalse(result)  # Should be case-sensitive
    
    @patch('email_mock.MockEmailService.send_email')
    def test_validate_user_multiple_users_finds_correct_one(self, mock_send):
        """Test validating finds correct user among multiple users"""
        self.manager.create_user("user1", "user1@test.com", "pass1pass", "customer")
        self.manager.create_user("user2", "user2@test.com", "pass2pass", "premium")
        self.manager.create_user("user3", "user3@test.com", "pass3pass", "vip")
        
        result = self.manager.validate_user("user2", "pass2pass")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
