import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from order_processor import OrderProcessor


class TestOrderProcessor(unittest.TestCase):
    """Comprehensive tests for OrderProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = OrderProcessor()
    
    def tearDown(self):
        """Clean up after tests"""
        self.processor = None
    
    # Test __init__
    def test_init_creates_empty_orders_list(self):
        """Test that initialization creates empty orders list"""
        self.assertEqual(self.processor.orders, [])
        self.assertIsInstance(self.processor.orders, list)
    
    def test_init_sets_order_id_counter(self):
        """Test that initialization sets order_id_counter to 1000"""
        self.assertEqual(self.processor.order_id_counter, 1000)
    
    def test_init_creates_email_service(self):
        """Test that initialization creates email service"""
        self.assertIsNotNone(self.processor.email_service)
    
    # Test process_order - successful customer credit card purchase
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_customer_credit_card_success(self, mock_print, mock_email, mock_ph):
        """Test successful customer order with credit card"""
        # Setup mock product handler
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        result = self.processor.process_order(user, "Laptop", 1, "credit_card")
        
        self.assertTrue(result)
        self.assertEqual(len(self.processor.orders), 1)
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_creates_order_with_correct_fields(self, mock_print, mock_email, mock_ph):
        """Test order is created with correct fields"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Laptop", 2, "credit_card")
        
        order = self.processor.orders[0]
        self.assertEqual(order["order_id"], 1000)
        self.assertEqual(order["user"], "john")
        self.assertEqual(order["product"], "Laptop")
        self.assertEqual(order["quantity"], 2)
        self.assertEqual(order["total"], 2000)  # customer pays full price
        self.assertEqual(order["status"], "confirmed")
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_customer_pays_full_price(self, mock_print, mock_email, mock_ph):
        """Test customer type pays full price"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Phone", "price": 500, "stock": 30}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Phone", 1, "credit_card")
        
        order = self.processor.orders[0]
        self.assertEqual(order["total"], 500)
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_decrements_stock(self, mock_print, mock_email, mock_ph):
        """Test processing order decrements product stock"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        product = {"name": "Laptop", "price": 1000, "stock": 50}
        mock_ph_instance.products = [product]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Laptop", 5, "credit_card")
        
        self.assertEqual(product["stock"], 45)
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_increments_order_id_counter(self, mock_print, mock_email, mock_ph):
        """Test processing order increments order_id_counter"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        
        self.assertEqual(self.processor.order_id_counter, 1001)
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_sends_confirmation_email(self, mock_print, mock_email, mock_ph):
        """Test processing order sends confirmation email"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        
        mock_email.assert_called_once()
        call_args = mock_email.call_args[0]
        self.assertEqual(call_args[0], "admin@shop.com")
        self.assertEqual(call_args[1], "john@test.com")
        self.assertIn("Order confirmed: 1000", call_args[2])
    
    # Test process_order - premium user discount
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_premium_gets_10_percent_discount(self, mock_print, mock_email, mock_ph):
        """Test premium user gets 10% discount (pays 90%)"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "premium", "email": "premium@test.com", "type": "premium"}
        
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        
        order = self.processor.orders[0]
        self.assertEqual(order["total"], 900)
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_premium_multiple_quantity(self, mock_print, mock_email, mock_ph):
        """Test premium discount with multiple quantity"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Phone", "price": 500, "stock": 30}
        ]
        
        user = {"username": "premium", "email": "premium@test.com", "type": "premium"}
        
        self.processor.process_order(user, "Phone", 2, "credit_card")
        
        order = self.processor.orders[0]
        self.assertEqual(order["total"], 900)  # 500 * 2 * 0.9
    
    # Test process_order - VIP user discount
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_vip_gets_20_percent_discount(self, mock_print, mock_email, mock_ph):
        """Test VIP user gets 20% discount (pays 80%)"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "vip", "email": "vip@test.com", "type": "vip"}
        
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        
        order = self.processor.orders[0]
        self.assertEqual(order["total"], 800)
    
    # Test process_order - PayPal payment method
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_paypal_payment_success(self, mock_print, mock_email, mock_ph):
        """Test successful order with PayPal payment"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        result = self.processor.process_order(user, "Laptop", 1, "paypal")
        
        self.assertTrue(result)
        self.assertEqual(len(self.processor.orders), 1)
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_order_paypal_prints_message(self, mock_print, mock_email, mock_ph):
        """Test PayPal payment prints correct message"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Laptop", 1, "paypal")
        
        mock_print.assert_called_with("Processing PayPal payment...")
    
    # Test process_order - validation failures
    @patch('product_handler.ProductHandler')
    def test_process_order_none_user_returns_false(self, mock_ph):
        """Test None user returns False"""
        result = self.processor.process_order(None, "Laptop", 1, "credit_card")
        self.assertFalse(result)
    
    @patch('product_handler.ProductHandler')
    def test_process_order_empty_product_name_returns_false(self, mock_ph):
        """Test empty product name returns False"""
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "", 1, "credit_card")
        self.assertFalse(result)
    
    @patch('product_handler.ProductHandler')
    def test_process_order_none_product_name_returns_false(self, mock_ph):
        """Test None product name returns False"""
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, None, 1, "credit_card")
        self.assertFalse(result)
    
    @patch('product_handler.ProductHandler')
    def test_process_order_zero_quantity_returns_false(self, mock_ph):
        """Test zero quantity returns False"""
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Laptop", 0, "credit_card")
        self.assertFalse(result)
    
    @patch('product_handler.ProductHandler')
    def test_process_order_negative_quantity_returns_false(self, mock_ph):
        """Test negative quantity returns False"""
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Laptop", -5, "credit_card")
        self.assertFalse(result)
    
    @patch('product_handler.ProductHandler')
    def test_process_order_none_payment_method_returns_false(self, mock_ph):
        """Test None payment method returns False"""
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Laptop", 1, None)
        self.assertFalse(result)
    
    @patch('product_handler.ProductHandler')
    def test_process_order_empty_payment_method_returns_false(self, mock_ph):
        """Test empty payment method returns False"""
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Laptop", 1, "")
        self.assertFalse(result)
    
    # Test process_order - product not found
    @patch('product_handler.ProductHandler')
    def test_process_order_nonexistent_product_returns_false(self, mock_ph):
        """Test ordering non-existent product returns False"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "NonExistent", 1, "credit_card")
        
        self.assertFalse(result)
    
    # Test process_order - insufficient stock
    @patch('product_handler.ProductHandler')
    def test_process_order_insufficient_stock_returns_false(self, mock_ph):
        """Test ordering more than available stock returns False"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 5}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Laptop", 10, "credit_card")
        
        self.assertFalse(result)
    
    @patch('product_handler.ProductHandler')
    def test_process_order_exact_stock_amount_succeeds(self, mock_ph):
        """Test ordering exactly available stock succeeds"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        product = {"name": "Laptop", "price": 1000, "stock": 5}
        mock_ph_instance.products = [product]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Laptop", 5, "credit_card")
        
        self.assertTrue(result)
        self.assertEqual(product["stock"], 0)
    
    # Test process_order - invalid payment method
    @patch('product_handler.ProductHandler')
    def test_process_order_invalid_payment_method_returns_false(self, mock_ph):
        """Test invalid payment method returns False"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Laptop", 1, "bitcoin")
        
        self.assertFalse(result)
    
    # Test process_order - zero price edge case
    @patch('product_handler.ProductHandler')
    def test_process_order_zero_price_returns_false(self, mock_ph):
        """Test product with zero price returns False"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Free", "price": 0, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        result = self.processor.process_order(user, "Free", 1, "credit_card")
        
        self.assertFalse(result)
    
    # Test multiple orders
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_multiple_orders(self, mock_print, mock_email, mock_ph):
        """Test processing multiple orders"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50},
            {"name": "Phone", "price": 500, "stock": 30}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        self.processor.process_order(user, "Phone", 1, "paypal")
        
        self.assertEqual(len(self.processor.orders), 2)
        self.assertEqual(self.processor.order_id_counter, 1002)
    
    @patch('product_handler.ProductHandler')
    @patch('email_mock.MockEmailService.send_email')
    @patch('builtins.print')
    def test_process_orders_have_unique_ids(self, mock_print, mock_email, mock_ph):
        """Test each order gets unique ID"""
        mock_ph_instance = MagicMock()
        mock_ph.return_value = mock_ph_instance
        mock_ph_instance.products = [
            {"name": "Laptop", "price": 1000, "stock": 50}
        ]
        
        user = {"username": "john", "email": "john@test.com", "type": "customer"}
        
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        self.processor.process_order(user, "Laptop", 1, "credit_card")
        
        order_ids = [order["order_id"] for order in self.processor.orders]
        self.assertEqual(order_ids, [1000, 1001, 1002])
        self.assertEqual(len(set(order_ids)), 3)  # All unique


if __name__ == '__main__':
    unittest.main()
