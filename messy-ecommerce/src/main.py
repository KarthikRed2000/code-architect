# Violates: Tight Coupling, No Dependency Injection
from user_manager import UserManager
from product_handler import ProductHandler
from order_processor import OrderProcessor
from payment_system import PaymentSystem

def main():
    # Create instances
    user_mgr = UserManager()
    product_handler = ProductHandler()
    order_proc = OrderProcessor()
    payment_sys = PaymentSystem()
    
    # Create users
    print("Setting up e-commerce system...")
    user_mgr.create_user("john_doe", "john@email.com", "password123", "customer")
    user_mgr.create_user("jane_vip", "jane@email.com", "securepass", "vip")
    
    # Add products
    print("Adding products...")
    product_handler.add_product("Laptop", 1200, "electronics", 50)
    product_handler.add_product("T-Shirt", 25, "clothing", 100)
    product_handler.add_product("Apple", 2, "food", 500)
    
    # Process orders
    print("Processing orders...")
    user = user_mgr.users[0]
    order_proc.process_order(user, "Laptop", 1, "credit_card")
    
    print("E-commerce system running...")

if __name__ == "__main__":
    main()
