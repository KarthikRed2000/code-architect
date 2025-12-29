# Violates: Single Responsibility, Long Methods
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
        report = "===== INVENTORY REPORT =====\n"
        
        for product, quantity in inventory.items():
            report += f"{product}: {quantity} units\n"
            
        report += "===========================\n"
        
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
