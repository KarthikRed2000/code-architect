import unittest
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from product_handler import ProductHandler


class TestProductHandler(unittest.TestCase):
    """Comprehensive tests for ProductHandler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = ProductHandler()
    
    def tearDown(self):
        """Clean up after tests"""
        self.handler = None
    
    # Test __init__
    def test_init_creates_empty_products_list(self):
        """Test that initialization creates empty products list"""
        self.assertEqual(self.handler.products, [])
        self.assertIsInstance(self.handler.products, list)
    
    def test_init_creates_empty_inventory_dict(self):
        """Test that initialization creates empty inventory dictionary"""
        self.assertEqual(self.handler.inventory, {})
        self.assertIsInstance(self.handler.inventory, dict)
    
    # Test add_product - electronics category
    def test_add_electronics_valid_above_100_with_stock(self):
        """Test adding valid electronics product > $100 with stock"""
        self.handler.add_product("Laptop", 1200, "electronics", 50)
        
        self.assertEqual(len(self.handler.products), 1)
        product = self.handler.products[0]
        self.assertEqual(product["name"], "Laptop")
        self.assertEqual(product["price"], 1200)
        self.assertEqual(product["category"], "electronics")
        self.assertEqual(product["stock"], 50)
        self.assertEqual(product["warranty"], "1 year")
        self.assertEqual(product["tax"], 1200 * 0.15)
        self.assertEqual(product["tax"], 180.0)
    
    def test_add_electronics_updates_inventory(self):
        """Test adding electronics product updates inventory"""
        self.handler.add_product("Phone", 500, "electronics", 30)
        
        self.assertIn("Phone", self.handler.inventory)
        self.assertEqual(self.handler.inventory["Phone"], 30)
    
    def test_add_electronics_exactly_100_not_added(self):
        """Test electronics at exactly $100 is not added"""
        self.handler.add_product("Item", 100, "electronics", 10)
        
        self.assertEqual(len(self.handler.products), 0)
        self.assertNotIn("Item", self.handler.inventory)
    
    def test_add_electronics_101_dollars_is_added(self):
        """Test electronics at $101 is added"""
        self.handler.add_product("Item", 101, "electronics", 10)
        
        self.assertEqual(len(self.handler.products), 1)
    
    def test_add_electronics_below_100_not_added(self):
        """Test electronics below $100 is not added"""
        self.handler.add_product("Cheap", 50, "electronics", 10)
        
        self.assertEqual(len(self.handler.products), 0)
        self.assertNotIn("Cheap", self.handler.inventory)
    
    def test_add_electronics_zero_stock_not_added(self):
        """Test electronics with zero stock is not added"""
        self.handler.add_product("Laptop", 1500, "electronics", 0)
        
        self.assertEqual(len(self.handler.products), 0)
    
    def test_add_electronics_negative_stock_not_added(self):
        """Test electronics with negative stock is not added"""
        self.handler.add_product("Laptop", 1500, "electronics", -5)
        
        self.assertEqual(len(self.handler.products), 0)
    
    # Test add_product - clothing category
    def test_add_clothing_valid_with_stock(self):
        """Test adding valid clothing product with stock"""
        self.handler.add_product("T-Shirt", 25, "clothing", 100)
        
        self.assertEqual(len(self.handler.products), 1)
        product = self.handler.products[0]
        self.assertEqual(product["name"], "T-Shirt")
        self.assertEqual(product["price"], 25)
        self.assertEqual(product["category"], "clothing")
        self.assertEqual(product["stock"], 100)
        self.assertEqual(product["warranty"], "30 days")
        self.assertEqual(product["tax"], 25 * 0.08)
        self.assertEqual(product["tax"], 2.0)
    
    def test_add_clothing_updates_inventory(self):
        """Test adding clothing product updates inventory"""
        self.handler.add_product("Jeans", 60, "clothing", 50)
        
        self.assertIn("Jeans", self.handler.inventory)
        self.assertEqual(self.handler.inventory["Jeans"], 50)
    
    def test_add_clothing_zero_price_not_added(self):
        """Test clothing with zero price is not added"""
        self.handler.add_product("Free", 0, "clothing", 10)
        
        self.assertEqual(len(self.handler.products), 0)
    
    def test_add_clothing_negative_price_not_added(self):
        """Test clothing with negative price is not added"""
        self.handler.add_product("Item", -5, "clothing", 10)
        
        self.assertEqual(len(self.handler.products), 0)
    
    def test_add_clothing_zero_stock_not_added(self):
        """Test clothing with zero stock is not added"""
        self.handler.add_product("Shirt", 30, "clothing", 0)
        
        self.assertEqual(len(self.handler.products), 0)
    
    def test_add_clothing_one_dollar_is_added(self):
        """Test clothing with $1 price is added"""
        self.handler.add_product("Socks", 1, "clothing", 100)
        
        self.assertEqual(len(self.handler.products), 1)
    
    # Test add_product - food category
    def test_add_food_valid_with_stock(self):
        """Test adding valid food product with stock"""
        self.handler.add_product("Apple", 2, "food", 500)
        
        self.assertEqual(len(self.handler.products), 1)
        product = self.handler.products[0]
        self.assertEqual(product["name"], "Apple")
        self.assertEqual(product["price"], 2)
        self.assertEqual(product["category"], "food")
        self.assertEqual(product["stock"], 500)
        self.assertEqual(product["warranty"], "none")
        self.assertEqual(product["tax"], 2 * 0.05)
        self.assertEqual(product["tax"], 0.1)
    
    def test_add_food_updates_inventory(self):
        """Test adding food product updates inventory"""
        self.handler.add_product("Banana", 1, "food", 200)
        
        self.assertIn("Banana", self.handler.inventory)
        self.assertEqual(self.handler.inventory["Banana"], 200)
    
    def test_add_food_zero_price_not_added(self):
        """Test food with zero price is not added"""
        self.handler.add_product("Free Sample", 0, "food", 100)
        
        self.assertEqual(len(self.handler.products), 0)
    
    def test_add_food_zero_stock_not_added(self):
        """Test food with zero stock is not added"""
        self.handler.add_product("Orange", 3, "food", 0)
        
        self.assertEqual(len(self.handler.products), 0)
    
    # Test add_product - unknown category
    def test_add_unknown_category_not_added(self):
        """Test product with unknown category is not added"""
        self.handler.add_product("Book", 20, "books", 50)
        
        self.assertEqual(len(self.handler.products), 0)
        self.assertNotIn("Book", self.handler.inventory)
    
    def test_add_empty_category_not_added(self):
        """Test product with empty category is not added"""
        self.handler.add_product("Item", 50, "", 10)
        
        self.assertEqual(len(self.handler.products), 0)
    
    # Test adding multiple products
    def test_add_multiple_products_different_categories(self):
        """Test adding multiple products from different categories"""
        self.handler.add_product("Laptop", 1200, "electronics", 50)
        self.handler.add_product("Shirt", 30, "clothing", 100)
        self.handler.add_product("Apple", 2, "food", 500)
        
        self.assertEqual(len(self.handler.products), 3)
        self.assertEqual(len(self.handler.inventory), 3)
    
    def test_add_multiple_products_same_category(self):
        """Test adding multiple products from same category"""
        self.handler.add_product("Laptop", 1200, "electronics", 50)
        self.handler.add_product("Phone", 500, "electronics", 30)
        self.handler.add_product("Tablet", 300, "electronics", 20)
        
        self.assertEqual(len(self.handler.products), 3)
    
    # Test get_product_price - customer type
    def test_get_product_price_customer_returns_full_price(self):
        """Test customer gets full product price"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        price = self.handler.get_product_price("Laptop", "customer")
        
        self.assertEqual(price, 1000)
    
    def test_get_product_price_customer_nonexistent_returns_zero(self):
        """Test customer gets 0 for non-existent product"""
        price = self.handler.get_product_price("NonExistent", "customer")
        self.assertEqual(price, 0)
    
    # Test get_product_price - premium type
    def test_get_product_price_premium_returns_90_percent(self):
        """Test premium user gets 10% discount (90% of price)"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        price = self.handler.get_product_price("Laptop", "premium")
        
        self.assertEqual(price, 900)
    
    def test_get_product_price_premium_float_calculation(self):
        """Test premium discount calculates correctly with floats"""
        self.handler.add_product("Item", 999, "electronics", 10)
        price = self.handler.get_product_price("Item", "premium")
        
        self.assertEqual(price, 999 * 0.9)
        self.assertAlmostEqual(price, 899.1, places=1)
    
    # Test get_product_price - vip type
    def test_get_product_price_vip_returns_80_percent(self):
        """Test VIP user gets 20% discount (80% of price)"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        price = self.handler.get_product_price("Laptop", "vip")
        
        self.assertEqual(price, 800)
    
    def test_get_product_price_vip_float_calculation(self):
        """Test VIP discount calculates correctly with floats"""
        self.handler.add_product("Item", 999, "electronics", 10)
        price = self.handler.get_product_price("Item", "vip")
        
        self.assertEqual(price, 999 * 0.8)
        self.assertAlmostEqual(price, 799.2, places=1)
    
    # Test get_product_price - unknown user type
    def test_get_product_price_unknown_user_type_returns_zero(self):
        """Test unknown user type returns 0"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        price = self.handler.get_product_price("Laptop", "unknown")
        
        self.assertEqual(price, 0)
    
    def test_get_product_price_empty_user_type_returns_zero(self):
        """Test empty user type returns 0"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        price = self.handler.get_product_price("Laptop", "")
        
        self.assertEqual(price, 0)
    
    # Test get_product_price with multiple products
    def test_get_product_price_finds_correct_product(self):
        """Test get_product_price finds correct product among multiple"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        self.handler.add_product("Phone", 500, "electronics", 30)
        self.handler.add_product("Tablet", 300, "electronics", 20)
        
        price = self.handler.get_product_price("Phone", "customer")
        self.assertEqual(price, 500)
    
    # Test tax calculations
    def test_electronics_tax_rate_15_percent(self):
        """Test electronics have 15% tax rate"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        product = self.handler.products[0]
        
        self.assertEqual(product["tax"], 150.0)
    
    def test_clothing_tax_rate_8_percent(self):
        """Test clothing has 8% tax rate"""
        self.handler.add_product("Shirt", 100, "clothing", 50)
        product = self.handler.products[0]
        
        self.assertEqual(product["tax"], 8.0)
    
    def test_food_tax_rate_5_percent(self):
        """Test food has 5% tax rate"""
        self.handler.add_product("Apple", 100, "food", 50)
        product = self.handler.products[0]
        
        self.assertEqual(product["tax"], 5.0)
    
    # Test warranty values
    def test_electronics_warranty_one_year(self):
        """Test electronics have 1 year warranty"""
        self.handler.add_product("Laptop", 1000, "electronics", 50)
        product = self.handler.products[0]
        
        self.assertEqual(product["warranty"], "1 year")
    
    def test_clothing_warranty_30_days(self):
        """Test clothing has 30 days warranty"""
        self.handler.add_product("Shirt", 30, "clothing", 50)
        product = self.handler.products[0]
        
        self.assertEqual(product["warranty"], "30 days")
    
    def test_food_warranty_none(self):
        """Test food has no warranty"""
        self.handler.add_product("Apple", 2, "food", 50)
        product = self.handler.products[0]
        
        self.assertEqual(product["warranty"], "none")


if __name__ == '__main__':
    unittest.main()
