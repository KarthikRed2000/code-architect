# Violates: Open/Closed Principle, Code Duplication
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
