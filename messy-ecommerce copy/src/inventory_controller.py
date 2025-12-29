# Violates: DRY, Single Responsibility
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
