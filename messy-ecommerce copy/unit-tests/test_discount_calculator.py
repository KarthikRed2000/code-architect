import unittest
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from discount_calculator import DiscountCalculator


class TestDiscountCalculator(unittest.TestCase):
    """Comprehensive tests for DiscountCalculator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calc = DiscountCalculator()
    
    def tearDown(self):
        """Clean up after tests"""
        self.calc = None
    
    # Test customer + electronics combinations
    def test_customer_electronics_over_1000_holiday(self):
        """Test customer buying electronics > $1000 on holiday"""
        discount = self.calc.calculate_discount("customer", "electronics", 1500, True)
        self.assertEqual(discount, 1500 * 0.15)
        self.assertEqual(discount, 225.0)
    
    def test_customer_electronics_over_1000_not_holiday(self):
        """Test customer buying electronics > $1000 not on holiday"""
        discount = self.calc.calculate_discount("customer", "electronics", 1500, False)
        self.assertEqual(discount, 1500 * 0.05)
        self.assertEqual(discount, 75.0)
    
    def test_customer_electronics_under_1000_holiday(self):
        """Test customer buying electronics < $1000 on holiday"""
        discount = self.calc.calculate_discount("customer", "electronics", 800, True)
        self.assertEqual(discount, 800 * 0.10)
        self.assertEqual(discount, 80.0)
    
    def test_customer_electronics_under_1000_not_holiday(self):
        """Test customer buying electronics < $1000 not on holiday"""
        discount = self.calc.calculate_discount("customer", "electronics", 800, False)
        self.assertEqual(discount, 800 * 0.02)
        self.assertEqual(discount, 16.0)
    
    def test_customer_electronics_exactly_1000_holiday(self):
        """Test customer buying electronics exactly $1000 on holiday"""
        discount = self.calc.calculate_discount("customer", "electronics", 1000, True)
        self.assertEqual(discount, 1000 * 0.10)  # Should use <= 1000 path
        self.assertEqual(discount, 100.0)
    
    def test_customer_electronics_exactly_1000_not_holiday(self):
        """Test customer buying electronics exactly $1000 not on holiday"""
        discount = self.calc.calculate_discount("customer", "electronics", 1000, False)
        self.assertEqual(discount, 1000 * 0.02)
        self.assertEqual(discount, 20.0)
    
    # Test customer + clothing combinations
    def test_customer_clothing_over_500_holiday(self):
        """Test customer buying clothing > $500 on holiday"""
        discount = self.calc.calculate_discount("customer", "clothing", 600, True)
        self.assertEqual(discount, 600 * 0.20)
        self.assertEqual(discount, 120.0)
    
    def test_customer_clothing_over_500_not_holiday(self):
        """Test customer buying clothing > $500 not on holiday"""
        discount = self.calc.calculate_discount("customer", "clothing", 600, False)
        self.assertEqual(discount, 600 * 0.10)
        self.assertEqual(discount, 60.0)
    
    def test_customer_clothing_under_500_holiday(self):
        """Test customer buying clothing < $500 on holiday"""
        discount = self.calc.calculate_discount("customer", "clothing", 300, True)
        self.assertEqual(discount, 300 * 0.15)
        self.assertEqual(discount, 45.0)
    
    def test_customer_clothing_under_500_not_holiday(self):
        """Test customer buying clothing < $500 not on holiday"""
        discount = self.calc.calculate_discount("customer", "clothing", 300, False)
        self.assertEqual(discount, 300 * 0.05)
        self.assertEqual(discount, 15.0)
    
    def test_customer_clothing_exactly_500_holiday(self):
        """Test customer buying clothing exactly $500 on holiday"""
        discount = self.calc.calculate_discount("customer", "clothing", 500, True)
        self.assertEqual(discount, 500 * 0.15)  # Should use <= 500 path
        self.assertEqual(discount, 75.0)
    
    def test_customer_clothing_exactly_500_not_holiday(self):
        """Test customer buying clothing exactly $500 not on holiday"""
        discount = self.calc.calculate_discount("customer", "clothing", 500, False)
        self.assertEqual(discount, 500 * 0.05)
        self.assertEqual(discount, 25.0)
    
    # Test premium + electronics combinations
    def test_premium_electronics_over_1000_holiday(self):
        """Test premium buying electronics > $1000 on holiday"""
        discount = self.calc.calculate_discount("premium", "electronics", 2000, True)
        self.assertEqual(discount, 2000 * 0.25)
        self.assertEqual(discount, 500.0)
    
    def test_premium_electronics_over_1000_not_holiday(self):
        """Test premium buying electronics > $1000 not on holiday"""
        discount = self.calc.calculate_discount("premium", "electronics", 2000, False)
        self.assertEqual(discount, 2000 * 0.15)
        self.assertEqual(discount, 300.0)
    
    def test_premium_electronics_under_1000_holiday(self):
        """Test premium buying electronics < $1000 on holiday"""
        discount = self.calc.calculate_discount("premium", "electronics", 500, True)
        self.assertEqual(discount, 500 * 0.20)
        self.assertEqual(discount, 100.0)
    
    def test_premium_electronics_under_1000_not_holiday(self):
        """Test premium buying electronics < $1000 not on holiday"""
        discount = self.calc.calculate_discount("premium", "electronics", 500, False)
        self.assertEqual(discount, 500 * 0.12)
        self.assertEqual(discount, 60.0)
    
    def test_premium_electronics_exactly_1000_holiday(self):
        """Test premium buying electronics exactly $1000 on holiday"""
        discount = self.calc.calculate_discount("premium", "electronics", 1000, True)
        self.assertEqual(discount, 1000 * 0.20)
        self.assertEqual(discount, 200.0)
    
    def test_premium_electronics_exactly_1000_not_holiday(self):
        """Test premium buying electronics exactly $1000 not on holiday"""
        discount = self.calc.calculate_discount("premium", "electronics", 1000, False)
        self.assertEqual(discount, 1000 * 0.12)
        self.assertEqual(discount, 120.0)
    
    # Test premium + clothing combinations
    def test_premium_clothing_over_500_holiday(self):
        """Test premium buying clothing > $500 on holiday"""
        discount = self.calc.calculate_discount("premium", "clothing", 700, True)
        self.assertEqual(discount, 700 * 0.30)
        self.assertEqual(discount, 210.0)
    
    def test_premium_clothing_over_500_not_holiday(self):
        """Test premium buying clothing > $500 not on holiday"""
        discount = self.calc.calculate_discount("premium", "clothing", 700, False)
        self.assertEqual(discount, 700 * 0.20)
        self.assertEqual(discount, 140.0)
    
    def test_premium_clothing_under_500_holiday(self):
        """Test premium buying clothing < $500 on holiday"""
        discount = self.calc.calculate_discount("premium", "clothing", 400, True)
        self.assertEqual(discount, 400 * 0.25)
        self.assertEqual(discount, 100.0)
    
    def test_premium_clothing_under_500_not_holiday(self):
        """Test premium buying clothing < $500 not on holiday"""
        discount = self.calc.calculate_discount("premium", "clothing", 400, False)
        self.assertEqual(discount, 400 * 0.15)
        self.assertEqual(discount, 60.0)
    
    def test_premium_clothing_exactly_500_holiday(self):
        """Test premium buying clothing exactly $500 on holiday"""
        discount = self.calc.calculate_discount("premium", "clothing", 500, True)
        self.assertEqual(discount, 500 * 0.25)
        self.assertEqual(discount, 125.0)
    
    def test_premium_clothing_exactly_500_not_holiday(self):
        """Test premium buying clothing exactly $500 not on holiday"""
        discount = self.calc.calculate_discount("premium", "clothing", 500, False)
        self.assertEqual(discount, 500 * 0.15)
        self.assertEqual(discount, 75.0)
    
    # Test VIP + electronics
    def test_vip_electronics_any_amount(self):
        """Test VIP buying electronics (flat 30% regardless of amount/holiday)"""
        discount = self.calc.calculate_discount("vip", "electronics", 1500, True)
        self.assertEqual(discount, 1500 * 0.30)
        self.assertEqual(discount, 450.0)
    
    def test_vip_electronics_not_holiday(self):
        """Test VIP buying electronics not on holiday (still 30%)"""
        discount = self.calc.calculate_discount("vip", "electronics", 1500, False)
        self.assertEqual(discount, 1500 * 0.30)
        self.assertEqual(discount, 450.0)
    
    def test_vip_electronics_small_amount(self):
        """Test VIP buying small amount of electronics"""
        discount = self.calc.calculate_discount("vip", "electronics", 100, True)
        self.assertEqual(discount, 100 * 0.30)
        self.assertEqual(discount, 30.0)
    
    # Test VIP + clothing
    def test_vip_clothing_any_amount(self):
        """Test VIP buying clothing (flat 35% regardless of amount/holiday)"""
        discount = self.calc.calculate_discount("vip", "clothing", 600, True)
        self.assertEqual(discount, 600 * 0.35)
        self.assertEqual(discount, 210.0)
    
    def test_vip_clothing_not_holiday(self):
        """Test VIP buying clothing not on holiday (still 35%)"""
        discount = self.calc.calculate_discount("vip", "clothing", 600, False)
        self.assertEqual(discount, 600 * 0.35)
        self.assertEqual(discount, 210.0)
    
    def test_vip_clothing_small_amount(self):
        """Test VIP buying small amount of clothing"""
        discount = self.calc.calculate_discount("vip", "clothing", 50, True)
        self.assertEqual(discount, 50 * 0.35)
        self.assertEqual(discount, 17.5)
    
    # Test unknown/invalid categories
    def test_customer_unknown_category_returns_zero(self):
        """Test customer with unknown category returns 0 discount"""
        discount = self.calc.calculate_discount("customer", "books", 1000, True)
        self.assertEqual(discount, 0)
    
    def test_premium_unknown_category_returns_zero(self):
        """Test premium with unknown category returns 0 discount"""
        discount = self.calc.calculate_discount("premium", "furniture", 2000, False)
        self.assertEqual(discount, 0)
    
    def test_vip_unknown_category_returns_zero(self):
        """Test VIP with unknown category returns 0 discount"""
        discount = self.calc.calculate_discount("vip", "groceries", 500, True)
        self.assertEqual(discount, 0)
    
    # Test unknown/invalid user types
    def test_unknown_user_type_returns_zero(self):
        """Test unknown user type returns 0 discount"""
        discount = self.calc.calculate_discount("guest", "electronics", 1000, True)
        self.assertEqual(discount, 0)
    
    def test_empty_user_type_returns_zero(self):
        """Test empty user type returns 0 discount"""
        discount = self.calc.calculate_discount("", "electronics", 1000, True)
        self.assertEqual(discount, 0)
    
    # Test edge cases with amounts
    def test_zero_order_total(self):
        """Test with zero order total"""
        discount = self.calc.calculate_discount("customer", "electronics", 0, True)
        self.assertEqual(discount, 0)
    
    def test_negative_order_total(self):
        """Test with negative order total"""
        discount = self.calc.calculate_discount("customer", "electronics", -100, True)
        # The code doesn't validate negative, so it will calculate negative discount
        expected = -100 * 0.10  # Under 1000, holiday
        self.assertEqual(discount, expected)
    
    def test_very_large_order_total(self):
        """Test with very large order total"""
        discount = self.calc.calculate_discount("vip", "electronics", 1000000, True)
        self.assertEqual(discount, 1000000 * 0.30)
        self.assertEqual(discount, 300000.0)
    
    def test_float_order_total(self):
        """Test with float order total"""
        discount = self.calc.calculate_discount("customer", "clothing", 599.99, True)
        self.assertEqual(discount, 599.99 * 0.20)
        self.assertAlmostEqual(discount, 119.998, places=2)
    
    # Test all combinations of boolean holiday parameter
    def test_holiday_true_is_handled(self):
        """Test that holiday=True is properly handled"""
        discount = self.calc.calculate_discount("customer", "electronics", 1500, True)
        self.assertGreater(discount, 0)
    
    def test_holiday_false_is_handled(self):
        """Test that holiday=False is properly handled"""
        discount = self.calc.calculate_discount("customer", "electronics", 1500, False)
        self.assertGreater(discount, 0)
    
    # Test boundary conditions
    def test_customer_electronics_1001_dollars(self):
        """Test just above $1000 threshold"""
        discount = self.calc.calculate_discount("customer", "electronics", 1001, True)
        self.assertEqual(discount, 1001 * 0.15)
    
    def test_customer_electronics_999_dollars(self):
        """Test just below $1000 threshold"""
        discount = self.calc.calculate_discount("customer", "electronics", 999, True)
        self.assertEqual(discount, 999 * 0.10)
    
    def test_customer_clothing_501_dollars(self):
        """Test just above $500 threshold"""
        discount = self.calc.calculate_discount("customer", "clothing", 501, True)
        self.assertEqual(discount, 501 * 0.20)
    
    def test_customer_clothing_499_dollars(self):
        """Test just below $500 threshold"""
        discount = self.calc.calculate_discount("customer", "clothing", 499, True)
        self.assertEqual(discount, 499 * 0.15)


if __name__ == '__main__':
    unittest.main()
