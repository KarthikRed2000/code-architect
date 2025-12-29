# Violates: Single Responsibility, Deep Nesting, Duplication
from email_mock import MockEmailService

class OrderProcessor:
    def __init__(self):
        self.orders = []
        self.order_id_counter = 1000
        self.email_service = MockEmailService()
        
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
                                            # Send email (mocked)
                                            message = f"Order confirmed: {order['order_id']}"
                                            self.email_service.send_email("admin@shop.com", user["email"], message)
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
                                            # Send email (mocked)
                                            message = f"Order confirmed: {order['order_id']}"
                                            self.email_service.send_email("admin@shop.com", user["email"], message)
                                            return True
        return False
