from model import create_and_train_model
from discount_logic import get_personalized_discount

def demo(user_id, location):
    model, user_mapping, shop_mapping = create_and_train_model()
    discounts = get_personalized_discount(user_id, user_mapping, shop_mapping, model)
    
    print(f"User {user_id} gets the following discounts:")
    for shop_name, discount in discounts.items():
        print(f"{shop_name}: {discount}")

    print("\nNearby shops:")
    nearby_shops = get_nearby_shops(location)
    for shop_name, shop_location in nearby_shops:
        print(f"{shop_name} at {shop_location}")

# Example usage
user_id = 1
location = (37.7749, -122.4194)
demo(user_id, location)
