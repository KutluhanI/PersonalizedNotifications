import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_user_data(num_users):
    user_data = pd.DataFrame({
        'user_id': np.arange(1, num_users + 1),
        'age': np.random.randint(18, 70, size=num_users),
        'gender': np.random.choice(['M', 'F'], size=num_users)
    })
    return user_data

def generate_shop_data(num_shops):
    shop_data = pd.DataFrame({
        'shop_id': np.arange(1, num_shops + 1),
        'category': np.random.choice(['electronics', 'fashion', 'grocery', 'home', 'sports'], size=num_shops)
    })
    return shop_data

def generate_purchase_history(user_data, shop_data, num_records):
    purchase_history = pd.DataFrame({
        'user_id': np.random.choice(user_data['user_id'], size=num_records),
        'shop_id': np.random.choice(shop_data['shop_id'], size=num_records),
        'items_bought': np.random.randint(1, 10, size=num_records),
        'amount_spent': np.random.randint(5, 500, size=num_records),
        'purchase_date': pd.date_range(start='2023-01-01', periods=num_records, freq='H')
    })
    return purchase_history

def generate_negative_samples(user_data, shop_data, num_records):
    negative_samples = pd.DataFrame({
        'user_id': np.random.choice(user_data['user_id'], size=num_records),
        'shop_id': np.random.choice(shop_data['shop_id'], size=num_records),
        'items_bought': 0,
        'amount_spent': 0,
        'purchase_date': pd.date_range(start='2023-01-01', periods=num_records, freq='H')
    })
    return negative_samples

def generate_mock_data(num_users, num_shops, num_records):
    user_data = generate_user_data(num_users)
    shop_data = generate_shop_data(num_shops)
    purchase_history = generate_purchase_history(user_data, shop_data, num_records)
    negative_samples = generate_negative_samples(user_data, shop_data, num_records)
    
    return user_data, shop_data, purchase_history, negative_samples

if __name__ == "__main__":
    num_users = 1000
    num_shops = 50
    num_records = 10000

    user_data, shop_data, purchase_history, negative_samples = generate_mock_data(num_users, num_shops, num_records)

    user_data.to_csv('./data/user_data.csv', index=False)
    shop_data.to_csv('./data/shop_data.csv', index=False)
    purchase_history.to_csv('data/purchase_history.csv', index=False)
    negative_samples.to_csv('data/negative_samples.csv', index=False)

    print(f"Generated {num_users} user data samples.")
    print(f"Generated {num_shops} shop data samples.")
    print(f"Generated {num_records} purchase history samples.")
    print(f"Generated {num_records} negative samples.")
