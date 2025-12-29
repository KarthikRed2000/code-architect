# Violates: Open/Closed, Complex Conditionals
class DiscountCalculator:
    def calculate_discount(self, user_type, product_category, order_total, is_holiday):
        discount = 0
        
        if user_type == "customer":
            if product_category == "electronics":
                if order_total > 1000:
                    if is_holiday:
                        discount = order_total * 0.15
                    else:
                        discount = order_total * 0.05
                else:
                    if is_holiday:
                        discount = order_total * 0.10
                    else:
                        discount = order_total * 0.02
            elif product_category == "clothing":
                if order_total > 500:
                    if is_holiday:
                        discount = order_total * 0.20
                    else:
                        discount = order_total * 0.10
                else:
                    if is_holiday:
                        discount = order_total * 0.15
                    else:
                        discount = order_total * 0.05
        elif user_type == "premium":
            if product_category == "electronics":
                if order_total > 1000:
                    if is_holiday:
                        discount = order_total * 0.25
                    else:
                        discount = order_total * 0.15
                else:
                    if is_holiday:
                        discount = order_total * 0.20
                    else:
                        discount = order_total * 0.12
            elif product_category == "clothing":
                if order_total > 500:
                    if is_holiday:
                        discount = order_total * 0.30
                    else:
                        discount = order_total * 0.20
                else:
                    if is_holiday:
                        discount = order_total * 0.25
                    else:
                        discount = order_total * 0.15
        elif user_type == "vip":
            if product_category == "electronics":
                discount = order_total * 0.30
            elif product_category == "clothing":
                discount = order_total * 0.35
                
        return discount
