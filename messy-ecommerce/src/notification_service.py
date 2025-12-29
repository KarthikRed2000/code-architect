# Violates: Code Duplication, Hardcoded Values
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
