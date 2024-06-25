import numpy as np
import pandas as pd

def get_personalized_discount(user_id, user_mapping, shop_mapping, model):
    def calculate_discount(prob):
        return f"{prob * 10:.1f}%"
    
    nearby_shops = pd.read_csv('../data/shop_data.csv')['shop_id'].tolist()
    discounts = {}
    for shop_name in nearby_shops:
        shop_id = shop_mapping.get(shop_name)
        if shop_id is not None:
            user_idx = user_mapping[user_id]
            shop_idx = shop_mapping[shop_id]
            prob = model.predict([np.array([user_idx]), np.array([shop_idx])])[0][0]
            discount = calculate_discount(prob)
            discounts[shop_name] = discount
    return discounts
