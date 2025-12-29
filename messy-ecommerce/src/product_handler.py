# Violates: Open/Closed, God Object, Tight Coupling
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
