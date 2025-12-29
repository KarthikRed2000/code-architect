#!/usr/bin/env python3
"""
Script to generate the messy e-commerce repository
Run: python generate_messy_repo.py
"""

import os

# File contents dictionary
files = {
    "user_manager.py": '''# Violates: Single Responsibility, DRY, Deep Nesting
class UserManager:
    def __init__(self):
        self.users = []
        self.db_connection = "mysql://localhost/ecommerce"
        
    def create_user(self, username, email, password, user_type):
        if username:
            if email:
                if password:
                    if len(password) >= 8:
                        if "@" in email:
                            if user_type == "customer":
                                user = {
                                    "username": username,
                                    "email": email,
                                    "password": password,
                                    "type": "customer",
                                    "discount": 0
                                }
                                self.users.append(user)
                                # Send email
                                import smtplib
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls()
                                server.login("admin@shop.com", "password123")
                                message = f"Welcome {username}!"
                                server.sendmail("admin@shop.com", email, message)
                                server.quit()
                                return True
                            elif user_type == "premium":
                                user = {
                                    "username": username,
                                    "email": email,
                                    "password": password,
                                    "type": "premium",
                                    "discount": 10
                                }
                                self.users.append(user)
                                # Send email
                                import smtplib
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls()
                                server.login("admin@shop.com", "password123")
                                message = f"Welcome Premium {username}!"
                                server.sendmail("admin@shop.com", email, message)
                                server.quit()
                                return True
                            elif user_type == "vip":
                                user = {
                                    "username": username,
                                    "email": email,
                                    "password": password,
                                    "type": "vip",
                                    "discount": 20
                                }
                                self.users.append(user)
                                # Send email
                                import smtplib
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls()
                                server.login("admin@shop.com", "password123")
                                message = f"Welcome VIP {username}!"
                                server.sendmail("admin@shop.com", email, message)
                                server.quit()
                                return True
        return False
    
    def validate_user(self, username, password):
        if username:
            if password:
                for user in self.users:
                    if user["username"] == username:
                        if user["password"] == password:
                            return True
        return False
''',

    "product_handler.py": '''# Violates: Open/Closed, God Object, Tight Coupling
class ProductHandler:
    def __init__(self):
        self.products = []
        self.inventory = {}
        
    def add_product(self, name, price, category, stock):
        if category == "electronics":
            if price > 100:
                if stock > 0:
                    product = {
                        "name": name,
                        "price": price,
                        "category": category,
                        "stock": stock,
                        "warranty": "1 year",
                        "tax": price * 0.15
                    }
                    self.products.append(product)
                    self.inventory[name] = stock
        elif category == "clothing":
            if price > 0:
                if stock > 0:
                    product = {
                        "name": name,
                        "price": price,
                        "category": category,
                        "stock": stock,
                        "warranty": "30 days",
                        "tax": price * 0.08
                    }
                    self.products.append(product)
                    self.inventory[name] = stock
        elif category == "food":
            if price > 0:
                if stock > 0:
                    product = {
                        "name": name,
                        "price": price,
                        "category": category,
                        "stock": stock,
                        "warranty": "none",
                        "tax": price * 0.05
                    }
                    self.products.append(product)
                    self.inventory[name] = stock
    
    def get_product_price(self, product_name, user_type):
        for product in self.products:
            if product["name"] == product_name:
                if user_type == "customer":
                    return product["price"]
                elif user_type == "premium":
                    return product["price"] * 0.9
                elif user_type == "vip":
                    return product["price"] * 0.8
        return 0
''',

    "order_processor.py": '''# Violates: Single Responsibility, Deep Nesting, Duplication
class OrderProcessor:
    def __init__(self):
        self.orders = []
        self.order_id_counter = 1000
        
    def process_order(self, user, product_name, quantity, payment_method):
        if user:
            if product_name:
                if quantity > 0:
                    if payment_method:
                        # Check inventory
                        from product_handler import ProductHandler
                        ph = ProductHandler()
                        for product in ph.products:
                            if product["name"] == product_name:
                                if product["stock"] >= quantity:
                                    # Calculate price
                                    if user["type"] == "customer":
                                        price = product["price"] * quantity
                                    elif user["type"] == "premium":
                                        price = product["price"] * quantity * 0.9
                                    elif user["type"] == "vip":
                                        price = product["price"] * quantity * 0.8
                                    
                                    # Process payment
                                    if payment_method == "credit_card":
                                        if price > 0:
                                            print("Processing credit card payment...")
                                            # Payment logic
                                            product["stock"] -= quantity
                                            order = {
                                                "order_id": self.order_id_counter,
                                                "user": user["username"],
                                                "product": product_name,
                                                "quantity": quantity,
                                                "total": price,
                                                "status": "confirmed"
                                            }
                                            self.orders.append(order)
                                            self.order_id_counter += 1
                                            # Send email
                                            import smtplib
                                            server = smtplib.SMTP('smtp.gmail.com', 587)
                                            server.starttls()
                                            server.login("admin@shop.com", "password123")
                                            message = f"Order confirmed: {order['order_id']}"
                                            server.sendmail("admin@shop.com", user["email"], message)
                                            server.quit()
                                            return True
                                    elif payment_method == "paypal":
                                        if price > 0:
                                            print("Processing PayPal payment...")
                                            # Payment logic
                                            product["stock"] -= quantity
                                            order = {
                                                "order_id": self.order_id_counter,
                                                "user": user["username"],
                                                "product": product_name,
                                                "quantity": quantity,
                                                "total": price,
                                                "status": "confirmed"
                                            }
                                            self.orders.append(order)
                                            self.order_id_counter += 1
                                            # Send email
                                            import smtplib
                                            server = smtplib.SMTP('smtp.gmail.com', 587)
                                            server.starttls()
                                            server.login("admin@shop.com", "password123")
                                            message = f"Order confirmed: {order['order_id']}"
                                            server.sendmail("admin@shop.com", user["email"], message)
                                            server.quit()
                                            return True
        return False
''',

    "payment_system.py": '''# Violates: Open/Closed Principle, Code Duplication
class PaymentSystem:
    def __init__(self):
        self.transactions = []
        
    def process_payment(self, amount, method, user_email):
        if method == "credit_card":
            if amount > 0:
                if amount < 10000:
                    print("Processing credit card...")
                    transaction = {
                        "amount": amount,
                        "method": "credit_card",
                        "status": "success",
                        "fee": amount * 0.03
                    }
                    self.transactions.append(transaction)
                    # Send confirmation
                    import smtplib
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login("admin@shop.com", "password123")
                    message = f"Payment of ${amount} processed"
                    server.sendmail("admin@shop.com", user_email, message)
                    server.quit()
                    return True
        elif method == "paypal":
            if amount > 0:
                if amount < 10000:
                    print("Processing PayPal...")
                    transaction = {
                        "amount": amount,
                        "method": "paypal",
                        "status": "success",
                        "fee": amount * 0.04
                    }
                    self.transactions.append(transaction)
                    # Send confirmation
                    import smtplib
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login("admin@shop.com", "password123")
                    message = f"Payment of ${amount} processed"
                    server.sendmail("admin@shop.com", user_email, message)
                    server.quit()
                    return True
        elif method == "bank_transfer":
            if amount > 0:
                if amount < 50000:
                    print("Processing bank transfer...")
                    transaction = {
                        "amount": amount,
                        "method": "bank_transfer",
                        "status": "pending",
                        "fee": amount * 0.01
                    }
                    self.transactions.append(transaction)
                    # Send confirmation
                    import smtplib
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login("admin@shop.com", "password123")
                    message = f"Payment of ${amount} processing"
                    server.sendmail("admin@shop.com", user_email, message)
                    server.quit()
                    return True
        return False
''',

    "inventory_controller.py": '''# Violates: DRY, Single Responsibility
class InventoryController:
    def __init__(self):
        self.inventory = {}
        self.low_stock_threshold = 10
        
    def update_inventory(self, product_name, quantity, operation):
        if operation == "add":
            if product_name in self.inventory:
                self.inventory[product_name] += quantity
                if self.inventory[product_name] < self.low_stock_threshold:
                    # Send alert
                    import smtplib
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login("admin@shop.com", "password123")
                    message = f"Low stock alert for {product_name}"
                    server.sendmail("admin@shop.com", "manager@shop.com", message)
                    server.quit()
            else:
                self.inventory[product_name] = quantity
        elif operation == "remove":
            if product_name in self.inventory:
                if self.inventory[product_name] >= quantity:
                    self.inventory[product_name] -= quantity
                    if self.inventory[product_name] < self.low_stock_threshold:
                        # Send alert
                        import smtplib
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login("admin@shop.com", "password123")
                        message = f"Low stock alert for {product_name}"
                        server.sendmail("admin@shop.com", "manager@shop.com", message)
                        server.quit()
        elif operation == "set":
            self.inventory[product_name] = quantity
            if self.inventory[product_name] < self.low_stock_threshold:
                # Send alert
                import smtplib
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("admin@shop.com", "password123")
                message = f"Low stock alert for {product_name}"
                server.sendmail("admin@shop.com", "manager@shop.com", message)
                server.quit()
''',

    "notification_service.py": '''# Violates: Code Duplication, Hardcoded Values
class NotificationService:
    def send_order_notification(self, user_email, order_id):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = f"Your order {order_id} has been placed"
        server.sendmail("admin@shop.com", user_email, message)
        server.quit()
        
    def send_shipping_notification(self, user_email, tracking_number):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = f"Your order has been shipped. Tracking: {tracking_number}"
        server.sendmail("admin@shop.com", user_email, message)
        server.quit()
        
    def send_delivery_notification(self, user_email):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = "Your order has been delivered"
        server.sendmail("admin@shop.com", user_email, message)
        server.quit()
        
    def send_cancellation_notification(self, user_email, order_id):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = f"Your order {order_id} has been cancelled"
        server.sendmail("admin@shop.com", user_email, message)
        server.quit()
''',

    "discount_calculator.py": '''# Violates: Open/Closed, Complex Conditionals
class DiscountCalculator:
    def calculate_discount(self, user_type, product_category, order_total, is_holiday):
        discount = 0
        
        if user_type == "customer":
            if product_category == "electronics":
                if order_total > 1000:
                    if is_holiday:
                        discount = order_total * 0.15
                    else:
                        discount = order_total * 0.05
                else:
                    if is_holiday:
                        discount = order_total * 0.10
                    else:
                        discount = order_total * 0.02
            elif product_category == "clothing":
                if order_total > 500:
                    if is_holiday:
                        discount = order_total * 0.20
                    else:
                        discount = order_total * 0.10
                else:
                    if is_holiday:
                        discount = order_total * 0.15
                    else:
                        discount = order_total * 0.05
        elif user_type == "premium":
            if product_category == "electronics":
                if order_total > 1000:
                    if is_holiday:
                        discount = order_total * 0.25
                    else:
                        discount = order_total * 0.15
                else:
                    if is_holiday:
                        discount = order_total * 0.20
                    else:
                        discount = order_total * 0.12
            elif product_category == "clothing":
                if order_total > 500:
                    if is_holiday:
                        discount = order_total * 0.30
                    else:
                        discount = order_total * 0.20
                else:
                    if is_holiday:
                        discount = order_total * 0.25
                    else:
                        discount = order_total * 0.15
        elif user_type == "vip":
            if product_category == "electronics":
                discount = order_total * 0.30
            elif product_category == "clothing":
                discount = order_total * 0.35
                
        return discount
''',

    "shipping_handler.py": '''# Violates: Many Responsibilities, Duplication
class ShippingHandler:
    def __init__(self):
        self.shipments = []
        
    def calculate_shipping(self, weight, destination, shipping_speed):
        cost = 0
        
        if destination == "domestic":
            if shipping_speed == "standard":
                if weight < 1:
                    cost = 5
                elif weight < 5:
                    cost = 10
                elif weight < 10:
                    cost = 15
                else:
                    cost = 25
            elif shipping_speed == "express":
                if weight < 1:
                    cost = 15
                elif weight < 5:
                    cost = 25
                elif weight < 10:
                    cost = 35
                else:
                    cost = 50
        elif destination == "international":
            if shipping_speed == "standard":
                if weight < 1:
                    cost = 20
                elif weight < 5:
                    cost = 40
                elif weight < 10:
                    cost = 60
                else:
                    cost = 100
            elif shipping_speed == "express":
                if weight < 1:
                    cost = 50
                elif weight < 5:
                    cost = 80
                elif weight < 10:
                    cost = 120
                else:
                    cost = 200
                    
        return cost
    
    def create_shipment(self, order_id, address, tracking_number):
        shipment = {
            "order_id": order_id,
            "address": address,
            "tracking": tracking_number,
            "status": "pending"
        }
        self.shipments.append(shipment)
''',

    "database_manager.py": '''# Violates: God Object, No Abstraction
class DatabaseManager:
    def __init__(self):
        self.connection = "mysql://localhost/ecommerce"
        
    def save_user(self, user_data):
        # Hardcoded SQL
        query = f"INSERT INTO users VALUES ('{user_data['username']}', '{user_data['email']}', '{user_data['password']}')"
        print(f"Executing: {query}")
        
    def save_product(self, product_data):
        query = f"INSERT INTO products VALUES ('{product_data['name']}', {product_data['price']}, '{product_data['category']}')"
        print(f"Executing: {query}")
        
    def save_order(self, order_data):
        query = f"INSERT INTO orders VALUES ({order_data['order_id']}, '{order_data['user']}', '{order_data['product']}', {order_data['quantity']})"
        print(f"Executing: {query}")
        
    def get_user(self, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        print(f"Executing: {query}")
        return None
        
    def get_all_products(self):
        query = "SELECT * FROM products"
        print(f"Executing: {query}")
        return []
        
    def update_inventory(self, product_name, quantity):
        query = f"UPDATE products SET stock = {quantity} WHERE name = '{product_name}'"
        print(f"Executing: {query}")
        
    def delete_user(self, username):
        query = f"DELETE FROM users WHERE username = '{username}'"
        print(f"Executing: {query}")
''',

    "report_generator.py": '''# Violates: Single Responsibility, Long Methods
class ReportGenerator:
    def generate_sales_report(self, orders, start_date, end_date):
        total_sales = 0
        total_orders = 0
        
        for order in orders:
            if True:  # Date check removed for simplicity
                total_sales += order["total"]
                total_orders += 1
        
        report = f"""
        ===== SALES REPORT =====
        Period: {start_date} to {end_date}
        Total Orders: {total_orders}
        Total Sales: ${total_sales}
        Average Order: ${total_sales / total_orders if total_orders > 0 else 0}
        ========================
        """
        
        # Save to file
        with open("sales_report.txt", "w") as f:
            f.write(report)
            
        # Send email
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        server.sendmail("admin@shop.com", "manager@shop.com", report)
        server.quit()
        
        return report
    
    def generate_inventory_report(self, inventory):
        report = "===== INVENTORY REPORT =====\\n"
        
        for product, quantity in inventory.items():
            report += f"{product}: {quantity} units\\n"
            
        report += "===========================\\n"
        
        # Save to file
        with open("inventory_report.txt", "w") as f:
            f.write(report)
            
        # Send email
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        server.sendmail("admin@shop.com", "manager@shop.com", report)
        server.quit()
        
        return report
''',

    "auth_system.py": '''# Violates: Security Best Practices, Deep Nesting
class AuthSystem:
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
        
    def login(self, username, password):
        if username:
            if password:
                if username not in self.failed_attempts:
                    self.failed_attempts[username] = 0
                    
                if self.failed_attempts[username] < 5:
                    # Check credentials (hardcoded for demo)
                    if username == "admin" and password == "admin123":
                        session_token = f"session_{username}_12345"
                        self.sessions[session_token] = username
                        self.failed_attempts[username] = 0
                        return session_token
                    else:
                        self.failed_attempts[username] += 1
                        if self.failed_attempts[username] >= 5:
                            # Send alert
                            import smtplib
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login("admin@shop.com", "password123")
                            message = f"Account locked for {username}"
                            server.sendmail("admin@shop.com", "security@shop.com", message)
                            server.quit()
                        return None
                else:
                    return "ACCOUNT_LOCKED"
        return None
    
    def logout(self, session_token):
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
''',

    "email_sender.py": '''# Violates: Code Duplication, Hardcoded Credentials
class EmailSender:
    def send_welcome_email(self, to_email, username):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = f"Welcome to our store, {username}!"
        server.sendmail("admin@shop.com", to_email, message)
        server.quit()
        
    def send_order_confirmation(self, to_email, order_id, total):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = f"Order {order_id} confirmed. Total: ${total}"
        server.sendmail("admin@shop.com", to_email, message)
        server.quit()
        
    def send_password_reset(self, to_email, reset_token):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = f"Reset your password: {reset_token}"
        server.sendmail("admin@shop.com", to_email, message)
        server.quit()
        
    def send_promotion(self, to_email, promo_code):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("admin@shop.com", "password123")
        message = f"Special offer! Use code: {promo_code}"
        server.sendmail("admin@shop.com", to_email, message)
        server.quit()
''',

    "main.py": '''# Violates: Tight Coupling, No Dependency Injection
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
    user_mgr.create_user("john_doe", "john@email.com", "password123", "customer")
    user_mgr.create_user("jane_vip", "jane@email.com", "securepass", "vip")
    
    # Add products
    product_handler.add_product("Laptop", 1200, "electronics", 50)
    product_handler.add_product("T-Shirt", 25, "clothing", 100)
    product_handler.add_product("Apple", 2, "food", 500)
    
    # Process orders
    user = user_mgr.users[0]
    order_proc.process_order(user, "Laptop", 1, "credit_card")
    
    print("E-commerce system running...")

if __name__ == "__main__":
    main()
''',

    "README.md": '''# Messy E-Commerce Repository

This is an intentionally messy codebase designed for practicing Low-Level Design (LLD) principles.

## 🎯 Purpose
Practice refactoring and applying SOLID principles, design patterns, and clean architecture.

## 📁 Structure
- 13 Python files with deep nesting, code duplication, and tight coupling
- Multiple SOLID violations
- Security issues and code smells

## 🚀 How to Use
1. Analyze the code for violations
2. Identify anti-patterns
3. Refactor using LLD principles
4. Apply appropriate design patterns
5. Implement clean architecture

## 🔍 Main Issues
- Single Responsibility violations
- Open/Closed principle violations
- Deep nesting (arrow anti-pattern)
- Code duplication (DRY violations)
- Tight coupling
- No dependency injection
- Hardcoded values
- Security vulnerabilities

## 💡 Suggested Improvements
- Extract interfaces
- Implement Strategy, Factory, Observer patterns
- Create repository pattern for database
- Add dependency injection
- Separate concerns into layers
- Add proper error handling
- Use configuration management

Happy refactoring! 🎓
'''
}

def create_directory_structure():
    """Create the project directory and all files"""
    project_dir = "messy-ecommerce"
    
    # Create main directory
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print(f"✓ Created directory: {project_dir}/")
    
    # Create all files
    for filename, content in files.items():
        filepath = os.path.join(project_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created: {filename}")
    
    print(f"\n✅ Successfully generated {len(files)} files in '{project_dir}/' directory!")
    print(f"\n📂 Navigate to the directory:")
    print(f"   cd {project_dir}")
    print(f"\n🚀 Start refactoring!")

if __name__ == "__main__":
    print("🗑️  Generating Messy E-Commerce Repository...\n")
    create_directory_structure()
