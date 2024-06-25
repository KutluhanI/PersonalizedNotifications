import pandas as pd
import numpy as np
import requests
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# Google Maps API Key
API_KEY = 'AIzaSyAr4jn5mcnSCX4jkLtUJDOffcE90WStvj0'

# Mock data
num_users = 100
num_shops = 50
num_records = 1000

user_data = pd.DataFrame({
    'user_id': np.arange(1, num_users + 1),
    'age': np.random.randint(18, 70, size=num_users),
    'gender': np.random.choice(['M', 'F'], size=num_users)
})

shop_data = pd.DataFrame({
    'shop_id': np.arange(1, num_shops + 1),
    'category': np.random.choice(['electronics', 'fashion', 'grocery', 'home', 'sports'], size=num_shops)
})

purchase_history = pd.DataFrame({
    'user_id': np.random.choice(user_data['user_id'], size=num_records),
    'shop_id': np.random.choice(shop_data['shop_id'], size=num_records),
    'items_bought': np.random.randint(1, 10, size=num_records),
    'amount_spent': np.random.randint(5, 500, size=num_records),
    'purchase_date': pd.date_range(start='2023-01-01', periods=num_records, freq='H')
})

# Generate negative samples
negative_samples = pd.DataFrame({
    'user_id': np.random.choice(user_data['user_id'], size=num_records),
    'shop_id': np.random.choice(shop_data['shop_id'], size=num_records),
    'items_bought': 0,
    'amount_spent': 0,
    'purchase_date': pd.date_range(start='2023-01-01', periods=num_records, freq='H')
})

# Combine positive and negative samples
purchase_history['label'] = 1
negative_samples['label'] = 0
full_data = pd.concat([purchase_history, negative_samples])

# Map user_id and shop_id to continuous ranges
user_mapping = {user_id: i for i, user_id in enumerate(user_data['user_id'].unique())}
shop_mapping = {shop_id: i for i, shop_id in enumerate(shop_data['shop_id'].unique())}

print("User Mapping:", user_mapping)
print("Shop Mapping:", shop_mapping)

full_data['user_id'] = full_data['user_id'].map(user_mapping)
full_data['shop_id'] = full_data['shop_id'].map(shop_mapping)

print("Mapped Full Data:")
print(full_data.head())

# Neural Collaborative Filtering Model

# Parameters
num_users = len(user_mapping)
num_shops = len(shop_mapping)
embedding_size = 50

# Input layers
user_input = Input(shape=(1,), name='user_input')
shop_input = Input(shape=(1,), name='shop_input')

# Embedding layers
user_embedding = Embedding(input_dim=num_users, output_dim=embedding_size, name='user_embedding')(user_input)
shop_embedding = Embedding(input_dim=num_shops, output_dim=embedding_size, name='shop_embedding')(shop_input)

# Flatten embeddings
user_vector = Flatten(name='user_flatten')(user_embedding)
shop_vector = Flatten(name='shop_flatten')(shop_embedding)

# Concatenate user and shop vectors
concat = Concatenate()([user_vector, shop_vector])

# Hidden layers
hidden = Dense(128, activation='relu')(concat)
hidden = Dense(64, activation='relu')(hidden)
output = Dense(1, activation='sigmoid')(hidden)

# Model
model = Model(inputs=[user_input, shop_input], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['AUC'])

# Summary
model.summary()

# Training the Model
# Example training data
user_input_data = full_data['user_id'].values
shop_input_data = full_data['shop_id'].values
labels = full_data['label'].values

# Split data into training and test sets
user_input_train, user_input_test, shop_input_train, shop_input_test, y_train, y_test = train_test_split(
    user_input_data, shop_input_data, labels, test_size=0.2, random_state=42)

# Train the model
model.fit([user_input_train, shop_input_train], y_train, epochs=10, batch_size=32, validation_data=([user_input_test, shop_input_test], y_test))

# Save the model
model.save('personalized_discount_model.keras')

# Evaluate the model
y_pred = model.predict([user_input_test, shop_input_test])
auc_score = roc_auc_score(y_test, y_pred)
print(f"AUC Score: {auc_score}")

# Google Maps API integration
def get_nearby_shops(location, radius=1500):
    lat, lng = location
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=store&key={API_KEY}"
    response = requests.get(url)
    results = response.json().get('results', [])
    shops = []
    for result in results:
        shop_name = result['name']
        shop_lat = result['geometry']['location']['lat']
        shop_lng = result['geometry']['location']['lng']
        shops.append((shop_name, (shop_lat, shop_lng)))
    return shops

# Personalized Discount Logic
def get_personalized_discount(user_id, location):
    nearby_shops = get_nearby_shops(location)
    discounts = {}
    for shop_name, shop_location in nearby_shops:
        shop_id = shop_mapping.get(shop_name)  # Assuming shop_name to shop_id mapping exists
        if shop_id is not None:
            user_idx = user_mapping[user_id]
            shop_idx = shop_mapping[shop_id]
            prob = model.predict([np.array([user_idx]), np.array([shop_idx])])
            discount = '10%' if prob > 0.5 else '5%'
            discounts[shop_name] = discount
    return discounts

# Example usage
user_id = 1
location = (37.7749, -122.4194)  # User's current location
discounts = get_personalized_discount(user_id, location)
print(f"User {user_id} gets the following discounts:")
for shop_name, discount in discounts.items():
    print(f"{shop_name}: {discount}")
