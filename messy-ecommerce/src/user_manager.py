# Violates: Single Responsibility, DRY, Deep Nesting
from email_mock import MockEmailService

class UserManager:
    def __init__(self):
        self.users = []
        self.db_connection = "mysql://localhost/ecommerce"
        self.email_service = MockEmailService()
        
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
                                # Send email (mocked)
                                message = f"Welcome {username}!"
                                self.email_service.send_email("admin@shop.com", email, message)
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
                                # Send email (mocked)
                                message = f"Welcome Premium {username}!"
                                self.email_service.send_email("admin@shop.com", email, message)
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
                                # Send email (mocked)
                                message = f"Welcome VIP {username}!"
                                self.email_service.send_email("admin@shop.com", email, message)
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
