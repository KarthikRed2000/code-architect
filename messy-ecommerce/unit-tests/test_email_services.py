import unittest
from unittest.mock import patch, MagicMock, call
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from email_sender import EmailSender
from notification_service import NotificationService


class TestEmailSender(unittest.TestCase):
    """Comprehensive tests for EmailSender class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sender = EmailSender()
    
    def tearDown(self):
        """Clean up after tests"""
        self.sender = None
    
    # Test send_welcome_email
    @patch('smtplib.SMTP')
    def test_send_welcome_email_creates_smtp_connection(self, mock_smtp):
        """Test that send_welcome_email creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_welcome_email("user@test.com", "TestUser")
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_welcome_email_starts_tls(self, mock_smtp):
        """Test that send_welcome_email starts TLS"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_welcome_email("user@test.com", "TestUser")
        
        mock_server.starttls.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_welcome_email_logs_in_with_credentials(self, mock_smtp):
        """Test that send_welcome_email logs in with hardcoded credentials"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_welcome_email("user@test.com", "TestUser")
        
        mock_server.login.assert_called_once_with("admin@shop.com", "password123")
    
    @patch('smtplib.SMTP')
    def test_send_welcome_email_sends_correct_message(self, mock_smtp):
        """Test that send_welcome_email sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_welcome_email("user@test.com", "John")
        
        # Check sendmail was called with correct parameters
        call_args = mock_server.sendmail.call_args[0]
        self.assertEqual(call_args[0], "admin@shop.com")
        self.assertEqual(call_args[1], "user@test.com")
        self.assertIn("Welcome to our store, John!", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_welcome_email_quits_connection(self, mock_smtp):
        """Test that send_welcome_email closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_welcome_email("user@test.com", "TestUser")
        
        mock_server.quit.assert_called_once()
    
    # Test send_order_confirmation
    @patch('smtplib.SMTP')
    def test_send_order_confirmation_creates_smtp_connection(self, mock_smtp):
        """Test that send_order_confirmation creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_order_confirmation("user@test.com", 12345, 99.99)
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_order_confirmation_sends_correct_message(self, mock_smtp):
        """Test that send_order_confirmation sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_order_confirmation("user@test.com", 12345, 150.50)
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Order 12345 confirmed", call_args[2])
        self.assertIn("$150.5", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_order_confirmation_quits_connection(self, mock_smtp):
        """Test that send_order_confirmation closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_order_confirmation("user@test.com", 12345, 99.99)
        
        mock_server.quit.assert_called_once()
    
    # Test send_password_reset
    @patch('smtplib.SMTP')
    def test_send_password_reset_creates_smtp_connection(self, mock_smtp):
        """Test that send_password_reset creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_password_reset("user@test.com", "token123")
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_password_reset_sends_correct_message(self, mock_smtp):
        """Test that send_password_reset sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_password_reset("user@test.com", "reset_token_xyz")
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Reset your password: reset_token_xyz", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_password_reset_quits_connection(self, mock_smtp):
        """Test that send_password_reset closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_password_reset("user@test.com", "token123")
        
        mock_server.quit.assert_called_once()
    
    # Test send_promotion
    @patch('smtplib.SMTP')
    def test_send_promotion_creates_smtp_connection(self, mock_smtp):
        """Test that send_promotion creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_promotion("user@test.com", "PROMO20")
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_promotion_sends_correct_message(self, mock_smtp):
        """Test that send_promotion sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_promotion("user@test.com", "SAVE50")
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Special offer! Use code: SAVE50", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_promotion_quits_connection(self, mock_smtp):
        """Test that send_promotion closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.sender.send_promotion("user@test.com", "PROMO20")
        
        mock_server.quit.assert_called_once()


class TestNotificationService(unittest.TestCase):
    """Comprehensive tests for NotificationService class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.service = NotificationService()
    
    def tearDown(self):
        """Clean up after tests"""
        self.service = None
    
    # Test send_order_notification
    @patch('smtplib.SMTP')
    def test_send_order_notification_creates_smtp_connection(self, mock_smtp):
        """Test that send_order_notification creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_order_notification("user@test.com", 1001)
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_order_notification_starts_tls(self, mock_smtp):
        """Test that send_order_notification starts TLS"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_order_notification("user@test.com", 1001)
        
        mock_server.starttls.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_order_notification_logs_in(self, mock_smtp):
        """Test that send_order_notification logs in"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_order_notification("user@test.com", 1001)
        
        mock_server.login.assert_called_once_with("admin@shop.com", "password123")
    
    @patch('smtplib.SMTP')
    def test_send_order_notification_sends_correct_message(self, mock_smtp):
        """Test that send_order_notification sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_order_notification("user@test.com", 5000)
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Your order 5000 has been placed", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_order_notification_quits_connection(self, mock_smtp):
        """Test that send_order_notification closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_order_notification("user@test.com", 1001)
        
        mock_server.quit.assert_called_once()
    
    # Test send_shipping_notification
    @patch('smtplib.SMTP')
    def test_send_shipping_notification_creates_smtp_connection(self, mock_smtp):
        """Test that send_shipping_notification creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_shipping_notification("user@test.com", "TRACK123")
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_shipping_notification_sends_correct_message(self, mock_smtp):
        """Test that send_shipping_notification sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_shipping_notification("user@test.com", "TRACK999")
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Your order has been shipped", call_args[2])
        self.assertIn("Tracking: TRACK999", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_shipping_notification_quits_connection(self, mock_smtp):
        """Test that send_shipping_notification closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_shipping_notification("user@test.com", "TRACK123")
        
        mock_server.quit.assert_called_once()
    
    # Test send_delivery_notification
    @patch('smtplib.SMTP')
    def test_send_delivery_notification_creates_smtp_connection(self, mock_smtp):
        """Test that send_delivery_notification creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_delivery_notification("user@test.com")
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_delivery_notification_sends_correct_message(self, mock_smtp):
        """Test that send_delivery_notification sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_delivery_notification("user@test.com")
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Your order has been delivered", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_delivery_notification_quits_connection(self, mock_smtp):
        """Test that send_delivery_notification closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_delivery_notification("user@test.com")
        
        mock_server.quit.assert_called_once()
    
    # Test send_cancellation_notification
    @patch('smtplib.SMTP')
    def test_send_cancellation_notification_creates_smtp_connection(self, mock_smtp):
        """Test that send_cancellation_notification creates SMTP connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_cancellation_notification("user@test.com", 2001)
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
    
    @patch('smtplib.SMTP')
    def test_send_cancellation_notification_sends_correct_message(self, mock_smtp):
        """Test that send_cancellation_notification sends correct message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_cancellation_notification("user@test.com", 3000)
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Your order 3000 has been cancelled", call_args[2])
    
    @patch('smtplib.SMTP')
    def test_send_cancellation_notification_quits_connection(self, mock_smtp):
        """Test that send_cancellation_notification closes connection"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.service.send_cancellation_notification("user@test.com", 2001)
        
        mock_server.quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
