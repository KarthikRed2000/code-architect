import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from payment_system import PaymentSystem


class TestPaymentSystem(unittest.TestCase):
    """Comprehensive tests for PaymentSystem class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.payment = PaymentSystem()
    
    def tearDown(self):
        """Clean up after tests"""
        self.payment = None
    
    # Test __init__
    def test_init_creates_empty_transactions_list(self):
        """Test that initialization creates empty transactions list"""
        self.assertEqual(self.payment.transactions, [])
        self.assertIsInstance(self.payment.transactions, list)
    
    # Test process_payment - credit card
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_valid_amount_returns_true(self, mock_print, mock_smtp):
        """Test processing credit card with valid amount returns True"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = self.payment.process_payment(100, "credit_card", "user@test.com")
        
        self.assertTrue(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_creates_transaction(self, mock_print, mock_smtp):
        """Test credit card payment creates transaction"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(100, "credit_card", "user@test.com")
        
        self.assertEqual(len(self.payment.transactions), 1)
        transaction = self.payment.transactions[0]
        self.assertEqual(transaction["amount"], 100)
        self.assertEqual(transaction["method"], "credit_card")
        self.assertEqual(transaction["status"], "success")
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_fee_is_3_percent(self, mock_print, mock_smtp):
        """Test credit card has 3% fee"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(1000, "credit_card", "user@test.com")
        
        transaction = self.payment.transactions[0]
        self.assertEqual(transaction["fee"], 1000 * 0.03)
        self.assertEqual(transaction["fee"], 30.0)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_prints_processing_message(self, mock_print, mock_smtp):
        """Test credit card prints processing message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(100, "credit_card", "user@test.com")
        
        mock_print.assert_called_with("Processing credit card...")
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_sends_confirmation_email(self, mock_print, mock_smtp):
        """Test credit card sends confirmation email"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(100, "credit_card", "user@test.com")
        
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called()
        mock_server.login.assert_called_with("admin@shop.com", "password123")
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Payment of $100 processed", call_args[2])
        mock_server.quit.assert_called()
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_zero_amount_returns_false(self, mock_print, mock_smtp):
        """Test credit card with zero amount returns False"""
        result = self.payment.process_payment(0, "credit_card", "user@test.com")
        self.assertFalse(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_negative_amount_returns_false(self, mock_print, mock_smtp):
        """Test credit card with negative amount returns False"""
        result = self.payment.process_payment(-50, "credit_card", "user@test.com")
        self.assertFalse(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_at_limit_9999_succeeds(self, mock_print, mock_smtp):
        """Test credit card at $9999 succeeds"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = self.payment.process_payment(9999, "credit_card", "user@test.com")
        self.assertTrue(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_at_10000_returns_false(self, mock_print, mock_smtp):
        """Test credit card at exactly $10000 returns False"""
        result = self.payment.process_payment(10000, "credit_card", "user@test.com")
        self.assertFalse(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_credit_card_above_10000_returns_false(self, mock_print, mock_smtp):
        """Test credit card above $10000 returns False"""
        result = self.payment.process_payment(15000, "credit_card", "user@test.com")
        self.assertFalse(result)
    
    # Test process_payment - paypal
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_paypal_valid_amount_returns_true(self, mock_print, mock_smtp):
        """Test processing PayPal with valid amount returns True"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = self.payment.process_payment(100, "paypal", "user@test.com")
        
        self.assertTrue(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_paypal_creates_transaction(self, mock_print, mock_smtp):
        """Test PayPal payment creates transaction"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(100, "paypal", "user@test.com")
        
        self.assertEqual(len(self.payment.transactions), 1)
        transaction = self.payment.transactions[0]
        self.assertEqual(transaction["amount"], 100)
        self.assertEqual(transaction["method"], "paypal")
        self.assertEqual(transaction["status"], "success")
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_paypal_fee_is_4_percent(self, mock_print, mock_smtp):
        """Test PayPal has 4% fee"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(1000, "paypal", "user@test.com")
        
        transaction = self.payment.transactions[0]
        self.assertEqual(transaction["fee"], 1000 * 0.04)
        self.assertEqual(transaction["fee"], 40.0)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_paypal_prints_processing_message(self, mock_print, mock_smtp):
        """Test PayPal prints processing message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(100, "paypal", "user@test.com")
        
        mock_print.assert_called_with("Processing PayPal...")
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_paypal_sends_confirmation_email(self, mock_print, mock_smtp):
        """Test PayPal sends confirmation email"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(200, "paypal", "user@test.com")
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Payment of $200 processed", call_args[2])
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_paypal_zero_amount_returns_false(self, mock_print, mock_smtp):
        """Test PayPal with zero amount returns False"""
        result = self.payment.process_payment(0, "paypal", "user@test.com")
        self.assertFalse(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_paypal_at_10000_returns_false(self, mock_print, mock_smtp):
        """Test PayPal at exactly $10000 returns False"""
        result = self.payment.process_payment(10000, "paypal", "user@test.com")
        self.assertFalse(result)
    
    # Test process_payment - bank transfer
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_valid_amount_returns_true(self, mock_print, mock_smtp):
        """Test processing bank transfer with valid amount returns True"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = self.payment.process_payment(1000, "bank_transfer", "user@test.com")
        
        self.assertTrue(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_creates_transaction(self, mock_print, mock_smtp):
        """Test bank transfer creates transaction"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(1000, "bank_transfer", "user@test.com")
        
        self.assertEqual(len(self.payment.transactions), 1)
        transaction = self.payment.transactions[0]
        self.assertEqual(transaction["amount"], 1000)
        self.assertEqual(transaction["method"], "bank_transfer")
        self.assertEqual(transaction["status"], "pending")
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_fee_is_1_percent(self, mock_print, mock_smtp):
        """Test bank transfer has 1% fee"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(10000, "bank_transfer", "user@test.com")
        
        transaction = self.payment.transactions[0]
        self.assertEqual(transaction["fee"], 10000 * 0.01)
        self.assertEqual(transaction["fee"], 100.0)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_status_is_pending(self, mock_print, mock_smtp):
        """Test bank transfer status is 'pending' not 'success'"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(1000, "bank_transfer", "user@test.com")
        
        transaction = self.payment.transactions[0]
        self.assertEqual(transaction["status"], "pending")
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_prints_processing_message(self, mock_print, mock_smtp):
        """Test bank transfer prints processing message"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(1000, "bank_transfer", "user@test.com")
        
        mock_print.assert_called_with("Processing bank transfer...")
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_sends_processing_email(self, mock_print, mock_smtp):
        """Test bank transfer sends 'processing' email not 'processed'"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(1000, "bank_transfer", "user@test.com")
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertIn("Payment of $1000 processing", call_args[2])
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_zero_amount_returns_false(self, mock_print, mock_smtp):
        """Test bank transfer with zero amount returns False"""
        result = self.payment.process_payment(0, "bank_transfer", "user@test.com")
        self.assertFalse(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_at_49999_succeeds(self, mock_print, mock_smtp):
        """Test bank transfer at $49999 succeeds"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = self.payment.process_payment(49999, "bank_transfer", "user@test.com")
        self.assertTrue(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_at_50000_returns_false(self, mock_print, mock_smtp):
        """Test bank transfer at exactly $50000 returns False"""
        result = self.payment.process_payment(50000, "bank_transfer", "user@test.com")
        self.assertFalse(result)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_bank_transfer_above_50000_returns_false(self, mock_print, mock_smtp):
        """Test bank transfer above $50000 returns False"""
        result = self.payment.process_payment(75000, "bank_transfer", "user@test.com")
        self.assertFalse(result)
    
    # Test invalid payment methods
    def test_invalid_payment_method_returns_false(self):
        """Test invalid payment method returns False"""
        result = self.payment.process_payment(100, "bitcoin", "user@test.com")
        self.assertFalse(result)
    
    def test_empty_payment_method_returns_false(self):
        """Test empty payment method returns False"""
        result = self.payment.process_payment(100, "", "user@test.com")
        self.assertFalse(result)
    
    # Test multiple transactions
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_multiple_transactions_are_stored(self, mock_print, mock_smtp):
        """Test multiple transactions are all stored"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.payment.process_payment(100, "credit_card", "user1@test.com")
        self.payment.process_payment(200, "paypal", "user2@test.com")
        self.payment.process_payment(300, "bank_transfer", "user3@test.com")
        
        self.assertEqual(len(self.payment.transactions), 3)
    
    @patch('smtplib.SMTP')
    @patch('builtins.print')
    def test_failed_payments_not_stored(self, mock_print, mock_smtp):
        """Test failed payments are not stored in transactions"""
        self.payment.process_payment(0, "credit_card", "user@test.com")
        self.payment.process_payment(100000, "paypal", "user@test.com")
        
        self.assertEqual(len(self.payment.transactions), 0)


if __name__ == '__main__':
    unittest.main()
