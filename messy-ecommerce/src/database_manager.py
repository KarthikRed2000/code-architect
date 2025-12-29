# Violates: God Object, No Abstraction
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
