# Violates: Code Duplication, Hardcoded Credentials
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
