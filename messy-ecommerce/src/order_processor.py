# Violates: Single Responsibility, Deep Nesting, Duplication
from email_mock import MockEmailService

from abc import ABC, abstractmethod

class MockEmailService:
    def send_email(self, sender, recipient, message):
        print(f"Sending email from {sender} to {recipient} with message: {message}")

class OrderProcessor:
    def __init__(self):
        self.orders = []
        self.order_id_counter = 1000
        self.email_service = MockEmailService()
        
    def process_order(self, user, product_name, quantity, payment_method):
        command = OrderCommandFactory.create_command(self, user, product_name, quantity, payment_method)
        if command:
            return command.execute()
        return False

class OrderCommand(ABC):
    def __init__(self, order_processor, user, product_name, quantity, payment_method):
        self.order_processor = order_processor
        self.user = user
        self.product_name = product_name
        self.quantity = quantity
        self.payment_method = payment_method

    @abstractmethod
    def execute(self):
        pass

class CreditCardOrderCommand(OrderCommand):
    def execute(self):
        if self.user:
            if self.product_name:
                if self.quantity > 0:
                    if self.payment_method == "credit_card":
                        from product_handler import ProductHandler
                        ph = ProductHandler()
                        for product in ph.products:
                            if product["name"] == self.product_name:
                                if product["stock"] >= self.quantity:
                                    if self.user["type"] == "customer":
                                        price = product["price"] * self.quantity
                                    elif self.user["type"] == "premium":
                                        price = product["price"] * self.quantity * 0.9
                                    elif self.user["type"] == "vip":
                                        price = product["price"] * self.quantity * 0.8
                                    if price > 0:
                                        print("Processing credit card payment...")
                                        product["stock"] -= self.quantity
                                        order = {
                                            "order_id": self.order_processor.order_id_counter,
                                            "user": self.user["username"],
                                            "product": self.product_name,
                                            "quantity": self.quantity,
                                            "total": price,
                                            "status": "confirmed"
                                        }
                                        self.order_processor.orders.append(order)
                                        self.order_processor.order_id_counter += 1
                                        message = f"Order confirmed: {order['order_id']}"
                                        self.order_processor.email_service.send_email("admin@shop.com", self.user["email"], message)
                                        return True
        return False

class PayPalOrderCommand(OrderCommand):
    def execute(self):
        if self.user:
            if self.product_name:
                if self.quantity > 0:
                    if self.payment_method == "paypal":
                        from product_handler import ProductHandler
                        ph = ProductHandler()
                        for product in ph.products:
                            if product["name"] == self.product_name:
                                if product["stock"] >= self.quantity:
                                    if self.user["type"] == "customer":
                                        price = product["price"] * self.quantity
                                    elif self.user["type"] == "premium":
                                        price = product["price"] * self.quantity * 0.9
                                    elif self.user["type"] == "vip":
                                        price = product["price"] * self.quantity * 0.8
                                    if price > 0:
                                        print("Processing PayPal payment...")
                                        product["stock"] -= self.quantity
                                        order = {
                                            "order_id": self.order_processor.order_id_counter,
                                            "user": self.user["username"],
                                            "product": self.product_name,
                                            "quantity": self.quantity,
                                            "total": price,
                                            "status": "confirmed"
                                        }
                                        self.order_processor.orders.append(order)
                                        self.order_processor.order_id_counter += 1
                                        message = f"Order confirmed: {order['order_id']}"
                                        self.order_processor.email_service.send_email("admin@shop.com", self.user["email"], message)
                                        return True
        return False

class OrderCommandFactory:
    @staticmethod
    def create_command(order_processor, user, product_name, quantity, payment_method):
        if payment_method == "credit_card":
            return CreditCardOrderCommand(order_processor, user, product_name, quantity, payment_method)
        elif payment_method == "paypal":
            return PayPalOrderCommand(order_processor, user, product_name, quantity, payment_method)
        else:
            return None
