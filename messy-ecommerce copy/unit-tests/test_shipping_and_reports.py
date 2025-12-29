import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from shipping_handler import ShippingHandler
from report_generator import ReportGenerator


class TestShippingHandler(unittest.TestCase):
    """Comprehensive tests for ShippingHandler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = ShippingHandler()
    
    def tearDown(self):
        """Clean up after tests"""
        self.handler = None
    
    # Test __init__
    def test_init_creates_empty_shipments_list(self):
        """Test that initialization creates empty shipments list"""
        self.assertEqual(self.handler.shipments, [])
        self.assertIsInstance(self.handler.shipments, list)
    
    # Test calculate_shipping - domestic standard
    def test_domestic_standard_under_1kg(self):
        """Test domestic standard shipping for weight < 1kg"""
        cost = self.handler.calculate_shipping(0.5, "domestic", "standard")
        self.assertEqual(cost, 5)
    
    def test_domestic_standard_1kg_to_5kg(self):
        """Test domestic standard shipping for 1kg <= weight < 5kg"""
        cost = self.handler.calculate_shipping(3, "domestic", "standard")
        self.assertEqual(cost, 10)
    
    def test_domestic_standard_5kg_to_10kg(self):
        """Test domestic standard shipping for 5kg <= weight < 10kg"""
        cost = self.handler.calculate_shipping(7, "domestic", "standard")
        self.assertEqual(cost, 15)
    
    def test_domestic_standard_10kg_or_more(self):
        """Test domestic standard shipping for weight >= 10kg"""
        cost = self.handler.calculate_shipping(15, "domestic", "standard")
        self.assertEqual(cost, 25)
    
    # Test boundary conditions for domestic standard
    def test_domestic_standard_exactly_1kg(self):
        """Test domestic standard at exactly 1kg boundary"""
        cost = self.handler.calculate_shipping(1, "domestic", "standard")
        self.assertEqual(cost, 10)
    
    def test_domestic_standard_exactly_5kg(self):
        """Test domestic standard at exactly 5kg boundary"""
        cost = self.handler.calculate_shipping(5, "domestic", "standard")
        self.assertEqual(cost, 15)
    
    def test_domestic_standard_exactly_10kg(self):
        """Test domestic standard at exactly 10kg boundary"""
        cost = self.handler.calculate_shipping(10, "domestic", "standard")
        self.assertEqual(cost, 25)
    
    # Test calculate_shipping - domestic express
    def test_domestic_express_under_1kg(self):
        """Test domestic express shipping for weight < 1kg"""
        cost = self.handler.calculate_shipping(0.5, "domestic", "express")
        self.assertEqual(cost, 15)
    
    def test_domestic_express_1kg_to_5kg(self):
        """Test domestic express shipping for 1kg <= weight < 5kg"""
        cost = self.handler.calculate_shipping(3, "domestic", "express")
        self.assertEqual(cost, 25)
    
    def test_domestic_express_5kg_to_10kg(self):
        """Test domestic express shipping for 5kg <= weight < 10kg"""
        cost = self.handler.calculate_shipping(7, "domestic", "express")
        self.assertEqual(cost, 35)
    
    def test_domestic_express_10kg_or_more(self):
        """Test domestic express shipping for weight >= 10kg"""
        cost = self.handler.calculate_shipping(15, "domestic", "express")
        self.assertEqual(cost, 50)
    
    # Test calculate_shipping - international standard
    def test_international_standard_under_1kg(self):
        """Test international standard shipping for weight < 1kg"""
        cost = self.handler.calculate_shipping(0.5, "international", "standard")
        self.assertEqual(cost, 20)
    
    def test_international_standard_1kg_to_5kg(self):
        """Test international standard shipping for 1kg <= weight < 5kg"""
        cost = self.handler.calculate_shipping(3, "international", "standard")
        self.assertEqual(cost, 40)
    
    def test_international_standard_5kg_to_10kg(self):
        """Test international standard shipping for 5kg <= weight < 10kg"""
        cost = self.handler.calculate_shipping(7, "international", "standard")
        self.assertEqual(cost, 60)
    
    def test_international_standard_10kg_or_more(self):
        """Test international standard shipping for weight >= 10kg"""
        cost = self.handler.calculate_shipping(15, "international", "standard")
        self.assertEqual(cost, 100)
    
    # Test calculate_shipping - international express
    def test_international_express_under_1kg(self):
        """Test international express shipping for weight < 1kg"""
        cost = self.handler.calculate_shipping(0.5, "international", "express")
        self.assertEqual(cost, 50)
    
    def test_international_express_1kg_to_5kg(self):
        """Test international express shipping for 1kg <= weight < 5kg"""
        cost = self.handler.calculate_shipping(3, "international", "express")
        self.assertEqual(cost, 80)
    
    def test_international_express_5kg_to_10kg(self):
        """Test international express shipping for 5kg <= weight < 10kg"""
        cost = self.handler.calculate_shipping(7, "international", "express")
        self.assertEqual(cost, 120)
    
    def test_international_express_10kg_or_more(self):
        """Test international express shipping for weight >= 10kg"""
        cost = self.handler.calculate_shipping(15, "international", "express")
        self.assertEqual(cost, 200)
    
    # Test invalid inputs
    def test_invalid_destination_returns_zero(self):
        """Test invalid destination returns 0"""
        cost = self.handler.calculate_shipping(5, "mars", "standard")
        self.assertEqual(cost, 0)
    
    def test_invalid_speed_returns_zero(self):
        """Test invalid shipping speed returns 0"""
        cost = self.handler.calculate_shipping(5, "domestic", "teleport")
        self.assertEqual(cost, 0)
    
    def test_zero_weight_returns_cost(self):
        """Test zero weight still processes (no validation)"""
        cost = self.handler.calculate_shipping(0, "domestic", "standard")
        self.assertEqual(cost, 5)  # Falls into < 1 category
    
    # Test create_shipment
    def test_create_shipment_adds_to_list(self):
        """Test create_shipment adds shipment to list"""
        self.handler.create_shipment(12345, "123 Main St", "TRACK123")
        
        self.assertEqual(len(self.handler.shipments), 1)
    
    def test_create_shipment_has_correct_fields(self):
        """Test created shipment has correct fields"""
        self.handler.create_shipment(12345, "123 Main St", "TRACK123")
        
        shipment = self.handler.shipments[0]
        self.assertEqual(shipment["order_id"], 12345)
        self.assertEqual(shipment["address"], "123 Main St")
        self.assertEqual(shipment["tracking"], "TRACK123")
        self.assertEqual(shipment["status"], "pending")
    
    def test_create_shipment_default_status_is_pending(self):
        """Test default shipment status is 'pending'"""
        self.handler.create_shipment(100, "Address", "TRACK")
        
        shipment = self.handler.shipments[0]
        self.assertEqual(shipment["status"], "pending")
    
    def test_create_multiple_shipments(self):
        """Test creating multiple shipments"""
        self.handler.create_shipment(101, "Address 1", "TRACK1")
        self.handler.create_shipment(102, "Address 2", "TRACK2")
        self.handler.create_shipment(103, "Address 3", "TRACK3")
        
        self.assertEqual(len(self.handler.shipments), 3)


class TestReportGenerator(unittest.TestCase):
    """Comprehensive tests for ReportGenerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = ReportGenerator()
    
    def tearDown(self):
        """Clean up after tests"""
        self.generator = None
    
    # Test generate_sales_report
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_sales_report_calculates_totals(self, mock_file, mock_smtp):
        """Test sales report calculates correct totals"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        orders = [
            {"total": 100},
            {"total": 200},
            {"total": 300}
        ]
        
        report = self.generator.generate_sales_report(orders, "2024-01-01", "2024-01-31")
        
        self.assertIn("Total Orders: 3", report)
        self.assertIn("Total Sales: $600", report)
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_sales_report_calculates_average(self, mock_file, mock_smtp):
        """Test sales report calculates correct average"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        orders = [
            {"total": 100},
            {"total": 200},
            {"total": 300}
        ]
        
        report = self.generator.generate_sales_report(orders, "2024-01-01", "2024-01-31")
        
        self.assertIn("Average Order: $200", report)
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_sales_report_with_zero_orders(self, mock_file, mock_smtp):
        """Test sales report with zero orders"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        orders = []
        
        report = self.generator.generate_sales_report(orders, "2024-01-01", "2024-01-31")
        
        self.assertIn("Total Orders: 0", report)
        self.assertIn("Total Sales: $0", report)
        self.assertIn("Average Order: $0", report)
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_sales_report_includes_period(self, mock_file, mock_smtp):
        """Test sales report includes date period"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        orders = [{"total": 100}]
        
        report = self.generator.generate_sales_report(orders, "2024-01-01", "2024-01-31")
        
        self.assertIn("Period: 2024-01-01 to 2024-01-31", report)
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_sales_report_saves_to_file(self, mock_file, mock_smtp):
        """Test sales report saves to file"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        orders = [{"total": 100}]
        
        self.generator.generate_sales_report(orders, "2024-01-01", "2024-01-31")
        
        mock_file.assert_called_with("sales_report.txt", "w")
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_sales_report_sends_email(self, mock_file, mock_smtp):
        """Test sales report sends email"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        orders = [{"total": 100}]
        
        self.generator.generate_sales_report(orders, "2024-01-01", "2024-01-31")
        
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called()
        mock_server.login.assert_called_with("admin@shop.com", "password123")
        mock_server.sendmail.assert_called()
        mock_server.quit.assert_called()
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_sales_report_returns_report_string(self, mock_file, mock_smtp):
        """Test sales report returns the report as string"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        orders = [{"total": 100}]
        
        report = self.generator.generate_sales_report(orders, "2024-01-01", "2024-01-31")
        
        self.assertIsInstance(report, str)
        self.assertIn("SALES REPORT", report)
    
    # Test generate_inventory_report
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_inventory_report_lists_all_products(self, mock_file, mock_smtp):
        """Test inventory report lists all products"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        inventory = {
            "Laptop": 50,
            "Phone": 30,
            "Tablet": 20
        }
        
        report = self.generator.generate_inventory_report(inventory)
        
        self.assertIn("Laptop: 50 units", report)
        self.assertIn("Phone: 30 units", report)
        self.assertIn("Tablet: 20 units", report)
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_inventory_report_with_empty_inventory(self, mock_file, mock_smtp):
        """Test inventory report with empty inventory"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        inventory = {}
        
        report = self.generator.generate_inventory_report(inventory)
        
        self.assertIn("INVENTORY REPORT", report)
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_inventory_report_saves_to_file(self, mock_file, mock_smtp):
        """Test inventory report saves to file"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        inventory = {"Product": 10}
        
        self.generator.generate_inventory_report(inventory)
        
        mock_file.assert_called_with("inventory_report.txt", "w")
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_inventory_report_sends_email(self, mock_file, mock_smtp):
        """Test inventory report sends email"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        inventory = {"Product": 10}
        
        self.generator.generate_inventory_report(inventory)
        
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called()
        mock_server.login.assert_called_with("admin@shop.com", "password123")
        call_args = mock_server.sendmail.call_args[0]
        self.assertEqual(call_args[0], "admin@shop.com")
        self.assertEqual(call_args[1], "manager@shop.com")
        mock_server.quit.assert_called()
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_inventory_report_returns_report_string(self, mock_file, mock_smtp):
        """Test inventory report returns the report as string"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        inventory = {"Product": 10}
        
        report = self.generator.generate_inventory_report(inventory)
        
        self.assertIsInstance(report, str)
        self.assertIn("INVENTORY REPORT", report)


if __name__ == '__main__':
    unittest.main()
