import pandas as pd
import numpy as np
import requests
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense

# Google Maps API Key
API_KEY = 'AIzaSyAr4jn5mcnSCX4jkLtUJDOffcE90WStvj0'

# Mock data
user_data = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5],
    'shop_id': [101, 102, 103, 104, 105],
    'items_bought': [5, 3, 6, 2, 4],
    'amount_spent': [100, 150, 200, 80, 120],
    'location': [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060), (51.5074, -0.1278), (48.8566, 2.3522)]
})

shop_data = pd.DataFrame({
    'shop_id': [101, 102, 103, 104, 105],
    'location': [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060), (51.5074, -0.1278), (48.8566, 2.3522)],
    'category': ['electronics', 'fashion', 'grocery', 'home', 'sports']
})

purchase_history = pd.DataFrame({
    'user_id': [1, 1, 2, 3, 4, 5, 5, 5],
    'shop_id': [101, 102, 102, 103, 104, 101, 103, 105],
    'items_bought': [1, 2, 1, 3, 2, 2, 1, 1],
    'purchase_date': pd.date_range(start='2023-01-01', periods=8, freq='M')
})

# Map user_id and shop_id to continuous ranges
user_mapping = {user_id: i for i, user_id in enumerate(user_data['user_id'].unique())}
shop_mapping = {shop_id: i for i, shop_id in enumerate(shop_data['shop_id'].unique())}

purchase_history['user_id'] = purchase_history['user_id'].map(user_mapping)
purchase_history['shop_id'] = purchase_history['shop_id'].map(shop_mapping)

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
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Summary
model.summary()

# Training the Model
# Example training data
train_data = {
    'user_input': purchase_history['user_id'].values,
    'shop_input': purchase_history['shop_id'].values
}
labels = np.ones(len(purchase_history))  # Assuming all interactions are positive

# Train the model
model.fit(train_data, labels, epochs=10, batch_size=2)

# Save the model
model.save('personalized_discount_model.h5')

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
