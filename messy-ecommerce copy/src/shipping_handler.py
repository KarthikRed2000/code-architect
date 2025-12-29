# Violates: Many Responsibilities, Duplication
class ShippingHandler:
    def __init__(self):
        self.shipments = []
        
    def calculate_shipping(self, weight, destination, shipping_speed):
        cost = 0
        
        if destination == "domestic":
            if shipping_speed == "standard":
                if weight < 1:
                    cost = 5
                elif weight < 5:
                    cost = 10
                elif weight < 10:
                    cost = 15
                else:
                    cost = 25
            elif shipping_speed == "express":
                if weight < 1:
                    cost = 15
                elif weight < 5:
                    cost = 25
                elif weight < 10:
                    cost = 35
                else:
                    cost = 50
        elif destination == "international":
            if shipping_speed == "standard":
                if weight < 1:
                    cost = 20
                elif weight < 5:
                    cost = 40
                elif weight < 10:
                    cost = 60
                else:
                    cost = 100
            elif shipping_speed == "express":
                if weight < 1:
                    cost = 50
                elif weight < 5:
                    cost = 80
                elif weight < 10:
                    cost = 120
                else:
                    cost = 200
                    
        return cost
    
    def create_shipment(self, order_id, address, tracking_number):
        shipment = {
            "order_id": order_id,
            "address": address,
            "tracking": tracking_number,
            "status": "pending"
        }
        self.shipments.append(shipment)
