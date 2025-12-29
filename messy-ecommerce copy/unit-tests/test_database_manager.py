import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Comprehensive tests for DatabaseManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = DatabaseManager()
    
    def tearDown(self):
        """Clean up after tests"""
        self.db = None
    
    # Test __init__
    def test_init_sets_connection_string(self):
        """Test that initialization sets connection string"""
        self.assertEqual(self.db.connection, "mysql://localhost/ecommerce")
    
    def test_init_connection_is_string(self):
        """Test that connection is a string"""
        self.assertIsInstance(self.db.connection, str)
    
    # Test save_user
    @patch('builtins.print')
    def test_save_user_with_all_fields(self, mock_print):
        """Test save_user with complete user data"""
        user_data = {
            'username': 'john_doe',
            'email': 'john@email.com',
            'password': 'secret123'
        }
        self.db.save_user(user_data)
        
        # Verify SQL was printed
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("INSERT INTO users", call_args)
        self.assertIn("john_doe", call_args)
        self.assertIn("john@email.com", call_args)
        self.assertIn("secret123", call_args)
    
    @patch('builtins.print')
    def test_save_user_constructs_correct_sql(self, mock_print):
        """Test that save_user constructs proper SQL query"""
        user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'pass'
        }
        self.db.save_user(user_data)
        
        expected = "Executing: INSERT INTO users VALUES ('testuser', 'test@test.com', 'pass')"
        mock_print.assert_called_with(expected)
    
    @patch('builtins.print')
    def test_save_user_with_special_characters(self, mock_print):
        """Test save_user handles special characters in data"""
        user_data = {
            'username': "user'with'quotes",
            'email': 'special@email.com',
            'password': 'p@ss!word'
        }
        self.db.save_user(user_data)
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("user'with'quotes", call_args)
        self.assertIn("p@ss!word", call_args)
    
    # Test save_product
    @patch('builtins.print')
    def test_save_product_with_all_fields(self, mock_print):
        """Test save_product with complete product data"""
        product_data = {
            'name': 'Laptop',
            'price': 1200,
            'category': 'electronics'
        }
        self.db.save_product(product_data)
        
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("INSERT INTO products", call_args)
        self.assertIn("Laptop", call_args)
        self.assertIn("1200", call_args)
        self.assertIn("electronics", call_args)
    
    @patch('builtins.print')
    def test_save_product_constructs_correct_sql(self, mock_print):
        """Test that save_product constructs proper SQL query"""
        product_data = {
            'name': 'Phone',
            'price': 500,
            'category': 'electronics'
        }
        self.db.save_product(product_data)
        
        expected = "Executing: INSERT INTO products VALUES ('Phone', 500, 'electronics')"
        mock_print.assert_called_with(expected)
    
    @patch('builtins.print')
    def test_save_product_with_float_price(self, mock_print):
        """Test save_product handles float prices"""
        product_data = {
            'name': 'Book',
            'price': 19.99,
            'category': 'books'
        }
        self.db.save_product(product_data)
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("19.99", call_args)
    
    @patch('builtins.print')
    def test_save_product_with_zero_price(self, mock_print):
        """Test save_product handles zero price"""
        product_data = {
            'name': 'Free Sample',
            'price': 0,
            'category': 'samples'
        }
        self.db.save_product(product_data)
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("0", call_args)
    
    # Test save_order
    @patch('builtins.print')
    def test_save_order_with_all_fields(self, mock_print):
        """Test save_order with complete order data"""
        order_data = {
            'order_id': 1001,
            'user': 'john_doe',
            'product': 'Laptop',
            'quantity': 2
        }
        self.db.save_order(order_data)
        
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("INSERT INTO orders", call_args)
        self.assertIn("1001", call_args)
        self.assertIn("john_doe", call_args)
        self.assertIn("Laptop", call_args)
        self.assertIn("2", call_args)
    
    @patch('builtins.print')
    def test_save_order_constructs_correct_sql(self, mock_print):
        """Test that save_order constructs proper SQL query"""
        order_data = {
            'order_id': 5000,
            'user': 'testuser',
            'product': 'Mouse',
            'quantity': 1
        }
        self.db.save_order(order_data)
        
        expected = "Executing: INSERT INTO orders VALUES (5000, 'testuser', 'Mouse', 1)"
        mock_print.assert_called_with(expected)
    
    @patch('builtins.print')
    def test_save_order_with_large_quantity(self, mock_print):
        """Test save_order handles large quantities"""
        order_data = {
            'order_id': 2000,
            'user': 'bulk_buyer',
            'product': 'Widget',
            'quantity': 10000
        }
        self.db.save_order(order_data)
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("10000", call_args)
    
    # Test get_user
    @patch('builtins.print')
    def test_get_user_constructs_correct_sql(self, mock_print):
        """Test that get_user constructs proper SQL query"""
        result = self.db.get_user('john_doe')
        
        expected = "Executing: SELECT * FROM users WHERE username = 'john_doe'"
        mock_print.assert_called_with(expected)
    
    @patch('builtins.print')
    def test_get_user_returns_none(self, mock_print):
        """Test that get_user returns None"""
        result = self.db.get_user('testuser')
        self.assertIsNone(result)
    
    @patch('builtins.print')
    def test_get_user_with_special_characters(self, mock_print):
        """Test get_user handles special characters"""
        self.db.get_user("user'with'quotes")
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("user'with'quotes", call_args)
    
    @patch('builtins.print')
    def test_get_user_with_empty_string(self, mock_print):
        """Test get_user with empty username"""
        result = self.db.get_user('')
        
        expected = "Executing: SELECT * FROM users WHERE username = ''"
        mock_print.assert_called_with(expected)
        self.assertIsNone(result)
    
    # Test get_all_products
    @patch('builtins.print')
    def test_get_all_products_constructs_correct_sql(self, mock_print):
        """Test that get_all_products constructs proper SQL query"""
        result = self.db.get_all_products()
        
        expected = "Executing: SELECT * FROM products"
        mock_print.assert_called_with(expected)
    
    @patch('builtins.print')
    def test_get_all_products_returns_empty_list(self, mock_print):
        """Test that get_all_products returns empty list"""
        result = self.db.get_all_products()
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
    
    # Test update_inventory
    @patch('builtins.print')
    def test_update_inventory_constructs_correct_sql(self, mock_print):
        """Test that update_inventory constructs proper SQL query"""
        self.db.update_inventory('Laptop', 50)
        
        expected = "Executing: UPDATE products SET stock = 50 WHERE name = 'Laptop'"
        mock_print.assert_called_with(expected)
    
    @patch('builtins.print')
    def test_update_inventory_with_zero_quantity(self, mock_print):
        """Test update_inventory with zero quantity"""
        self.db.update_inventory('Phone', 0)
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("stock = 0", call_args)
    
    @patch('builtins.print')
    def test_update_inventory_with_large_quantity(self, mock_print):
        """Test update_inventory with large quantity"""
        self.db.update_inventory('Widget', 999999)
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("999999", call_args)
    
    @patch('builtins.print')
    def test_update_inventory_with_special_characters_in_name(self, mock_print):
        """Test update_inventory handles special characters"""
        self.db.update_inventory("Product'with'quotes", 100)
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("Product'with'quotes", call_args)
    
    # Test delete_user
    @patch('builtins.print')
    def test_delete_user_constructs_correct_sql(self, mock_print):
        """Test that delete_user constructs proper SQL query"""
        self.db.delete_user('john_doe')
        
        expected = "Executing: DELETE FROM users WHERE username = 'john_doe'"
        mock_print.assert_called_with(expected)
    
    @patch('builtins.print')
    def test_delete_user_with_special_characters(self, mock_print):
        """Test delete_user handles special characters"""
        self.db.delete_user("user'with'quotes")
        
        call_args = mock_print.call_args[0][0]
        self.assertIn("user'with'quotes", call_args)
    
    @patch('builtins.print')
    def test_delete_user_with_empty_string(self, mock_print):
        """Test delete_user with empty username"""
        self.db.delete_user('')
        
        expected = "Executing: DELETE FROM users WHERE username = ''"
        mock_print.assert_called_with(expected)
    
    # Test SQL injection vulnerability (demonstrating the issue)
    @patch('builtins.print')
    def test_save_user_sql_injection_potential(self, mock_print):
        """Test demonstrates SQL injection vulnerability in save_user"""
        user_data = {
            'username': "'; DROP TABLE users; --",
            'email': 'hacker@evil.com',
            'password': 'pass'
        }
        self.db.save_user(user_data)
        
        call_args = mock_print.call_args[0][0]
        # This demonstrates the vulnerability
        self.assertIn("DROP TABLE users", call_args)


if __name__ == '__main__':
    unittest.main()
