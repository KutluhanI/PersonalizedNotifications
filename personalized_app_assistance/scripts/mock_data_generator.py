import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_mock_data(num_samples):
    customer_numbers = [fake.random_int(min=1000, max=9999) for _ in range(num_samples)]
    event_names = ['fx_market', 'borsa', 'kredi_basvuru', 'hesap_acma']
    categories = ['Finance', 'Banking']
    subcategories = {
        'Finance': ['Forex', 'Stock Market', 'Loans'],
        'Banking': ['Account Opening', 'Savings', 'Transfers']
    }

    data = []

    for i in range(num_samples):
        event_name = np.random.choice(event_names)
        category = 'Finance' if event_name in ['fx_market', 'borsa', 'kredi_basvuru'] else 'Banking'
        subcategory = np.random.choice(subcategories[category])
        data.append([
            customer_numbers[i],
            event_name,
            category,
            subcategory
        ])

    df = pd.DataFrame(data, columns=['customernumber', 'event_name', 'category', 'subcategory'])
    return df

def generate_mock_response_data(num_samples):
    customer_numbers = [fake.random_int(min=1000, max=9999) for _ in range(num_samples)]
    response_types = ['opened', 'dismissed', 'ignored']
    data = []

    for i in range(num_samples):
        notification_id = i + 1
        response_time = fake.random_int(min=1, max=60)
        response_type = np.random.choice(response_types)
        data.append([
            customer_numbers[i],
            notification_id,
            response_time,
            response_type
        ])

    df = pd.DataFrame(data, columns=['customernumber', 'notification_id', 'response_time', 'response_type'])
    return df

if __name__ == "__main__":
    num_samples = 10000

    mock_data = generate_mock_data(num_samples)
    mock_data.to_csv('data/mock_data.csv', index=False)
    print(f"Generated {num_samples} mock data samples.")

    mock_response_data = generate_mock_response_data(num_samples)
    mock_response_data.to_csv('data/mock_response_data.csv', index=False)
    print(f"Generated {num_samples} mock response data samples.")
