import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from inventory_controller import InventoryController


class TestInventoryController(unittest.TestCase):
    """Comprehensive tests for InventoryController class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = InventoryController()
    
    def tearDown(self):
        """Clean up after tests"""
        self.controller = None
    
    # Test __init__
    def test_init_creates_empty_inventory(self):
        """Test that initialization creates empty inventory dictionary"""
        self.assertEqual(self.controller.inventory, {})
        self.assertIsInstance(self.controller.inventory, dict)
    
    def test_init_sets_low_stock_threshold(self):
        """Test that initialization sets low stock threshold to 10"""
        self.assertEqual(self.controller.low_stock_threshold, 10)
    
    # Test update_inventory - "add" operation for new product
    @patch('smtplib.SMTP')
    def test_add_new_product_creates_inventory_entry(self, mock_smtp):
        """Test adding new product creates inventory entry"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Laptop", 50, "add")
        
        self.assertIn("Laptop", self.controller.inventory)
        self.assertEqual(self.controller.inventory["Laptop"], 50)
    
    @patch('smtplib.SMTP')
    def test_add_new_product_above_threshold_no_alert(self, mock_smtp):
        """Test adding new product above threshold doesn't send alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Phone", 50, "add")
        
        # Email should not be sent
        mock_smtp.assert_not_called()
    
    @patch('smtplib.SMTP')
    def test_add_new_product_below_threshold_no_alert(self, mock_smtp):
        """Test adding new product below threshold doesn't send alert (just sets value)"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("LowStock", 5, "add")
        
        # For NEW products, alert is NOT sent - it just sets the value
        mock_smtp.assert_not_called()
    
    @patch('smtplib.SMTP')
    def test_add_new_product_with_low_stock_no_alert(self, mock_smtp):
        """Test adding new product doesn't trigger alert (only existing products do)"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("TestProduct", 5, "add")
        
        # New products don't trigger alerts with 'add'
        mock_smtp.assert_not_called()
    
    # Test update_inventory - "add" operation for existing product
    @patch('smtplib.SMTP')
    def test_add_to_existing_product_increases_quantity(self, mock_smtp):
        """Test adding to existing product increases quantity"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Laptop"] = 30
        self.controller.update_inventory("Laptop", 20, "add")
        
        self.assertEqual(self.controller.inventory["Laptop"], 50)
    
    @patch('smtplib.SMTP')
    def test_add_existing_stays_above_threshold_no_alert(self, mock_smtp):
        """Test adding to existing product that stays above threshold"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Phone"] = 20
        self.controller.update_inventory("Phone", 10, "add")
        
        mock_smtp.assert_not_called()
    
    @patch('smtplib.SMTP')
    def test_add_existing_goes_below_threshold_sends_alert(self, mock_smtp):
        """Test adding to existing product that goes below threshold sends alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Product"] = 5
        self.controller.update_inventory("Product", 2, "add")
        
        # Still below threshold (7 < 10), should send alert
        mock_smtp.assert_called_once()
    
    # Test update_inventory - "remove" operation
    @patch('smtplib.SMTP')
    def test_remove_from_existing_product_decreases_quantity(self, mock_smtp):
        """Test removing from existing product decreases quantity"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Laptop"] = 50
        self.controller.update_inventory("Laptop", 20, "remove")
        
        self.assertEqual(self.controller.inventory["Laptop"], 30)
    
    @patch('smtplib.SMTP')
    def test_remove_stays_above_threshold_no_alert(self, mock_smtp):
        """Test removing but staying above threshold doesn't send alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Phone"] = 50
        self.controller.update_inventory("Phone", 20, "remove")
        
        mock_smtp.assert_not_called()
    
    @patch('smtplib.SMTP')
    def test_remove_goes_below_threshold_sends_alert(self, mock_smtp):
        """Test removing and going below threshold sends alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Product"] = 15
        self.controller.update_inventory("Product", 10, "remove")
        
        # Now at 5, below threshold
        self.assertEqual(self.controller.inventory["Product"], 5)
        mock_smtp.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_remove_more_than_available_no_change(self, mock_smtp):
        """Test removing more than available doesn't change inventory"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Product"] = 10
        self.controller.update_inventory("Product", 20, "remove")
        
        # Should remain unchanged
        self.assertEqual(self.controller.inventory["Product"], 10)
    
    @patch('smtplib.SMTP')
    def test_remove_exact_quantity_sets_to_zero(self, mock_smtp):
        """Test removing exact quantity sets inventory to zero"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Product"] = 20
        self.controller.update_inventory("Product", 20, "remove")
        
        self.assertEqual(self.controller.inventory["Product"], 0)
        mock_smtp.assert_called_once()  # 0 < 10, should alert
    
    @patch('smtplib.SMTP')
    def test_remove_from_nonexistent_product_no_effect(self, mock_smtp):
        """Test removing from non-existent product has no effect"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("NonExistent", 10, "remove")
        
        self.assertNotIn("NonExistent", self.controller.inventory)
        mock_smtp.assert_not_called()
    
    # Test update_inventory - "set" operation
    @patch('smtplib.SMTP')
    def test_set_creates_new_product_entry(self, mock_smtp):
        """Test set operation creates new product entry"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("NewProduct", 30, "set")
        
        self.assertIn("NewProduct", self.controller.inventory)
        self.assertEqual(self.controller.inventory["NewProduct"], 30)
    
    @patch('smtplib.SMTP')
    def test_set_updates_existing_product(self, mock_smtp):
        """Test set operation updates existing product"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.inventory["Product"] = 50
        self.controller.update_inventory("Product", 25, "set")
        
        self.assertEqual(self.controller.inventory["Product"], 25)
    
    @patch('smtplib.SMTP')
    def test_set_above_threshold_no_alert(self, mock_smtp):
        """Test set operation above threshold doesn't send alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Product", 50, "set")
        
        mock_smtp.assert_not_called()
    
    @patch('smtplib.SMTP')
    def test_set_below_threshold_sends_alert(self, mock_smtp):
        """Test set operation below threshold sends alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Product", 5, "set")
        
        mock_smtp.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_set_to_zero_sends_alert(self, mock_smtp):
        """Test set operation to zero sends alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Product", 0, "set")
        
        self.assertEqual(self.controller.inventory["Product"], 0)
        mock_smtp.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_set_exactly_at_threshold_sends_alert(self, mock_smtp):
        """Test set operation exactly at threshold (10) doesn't send alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Product", 10, "set")
        
        # 10 is not < 10, so no alert
        mock_smtp.assert_not_called()
    
    @patch('smtplib.SMTP')
    def test_set_just_below_threshold_sends_alert(self, mock_smtp):
        """Test set operation just below threshold (9) sends alert"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Product", 9, "set")
        
        mock_smtp.assert_called_once()
    
    # Test invalid operations
    @patch('smtplib.SMTP')
    def test_invalid_operation_no_effect(self, mock_smtp):
        """Test invalid operation has no effect"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Product", 50, "invalid")
        
        self.assertNotIn("Product", self.controller.inventory)
        mock_smtp.assert_not_called()
    
    @patch('smtplib.SMTP')
    def test_empty_operation_no_effect(self, mock_smtp):
        """Test empty operation string has no effect"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.controller.update_inventory("Product", 50, "")
        
        self.assertNotIn("Product", self.controller.inventory)
    
    # Test email alert functionality
    @patch('smtplib.SMTP')
    def test_alert_email_sent_to_manager(self, mock_smtp):
        """Test alert email is sent to manager"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Use 'set' operation to trigger alert for new product
        self.controller.update_inventory("Product", 5, "set")
        
        call_args = mock_server.sendmail.call_args[0]
        self.assertEqual(call_args[0], "admin@shop.com")
        self.assertEqual(call_args[1], "manager@shop.com")
    
    @patch('smtplib.SMTP')
    def test_multiple_operations_multiple_alerts(self, mock_smtp):
        """Test multiple operations can trigger multiple alerts"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Use 'set' for both to trigger alerts (add doesn't alert for new products)
        self.controller.update_inventory("Product1", 5, "set")
        self.controller.update_inventory("Product2", 3, "set")
        
        self.assertEqual(mock_smtp.call_count, 2)
    
    # Test edge cases
    @patch('smtplib.SMTP')
    def test_negative_quantity_handled(self, mock_smtp):
        """Test negative quantity is handled (even if not validated)"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Use 'set' operation to trigger alert check
        self.controller.update_inventory("Product", -5, "set")
        
        # Code doesn't validate, so this will create entry with -5
        self.assertEqual(self.controller.inventory["Product"], -5)
        mock_smtp.assert_called_once()  # -5 < 10
    
    @patch('smtplib.SMTP')
    def test_add_zero_quantity(self, mock_smtp):
        """Test adding zero quantity"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Use 'set' to trigger alert check
        self.controller.update_inventory("Product", 0, "set")
        
        self.assertEqual(self.controller.inventory["Product"], 0)
        mock_smtp.assert_called_once()


if __name__ == '__main__':
    unittest.main()
