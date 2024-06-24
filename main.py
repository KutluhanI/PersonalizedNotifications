import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense

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

# Personalized Discount Logic
def get_personalized_discount(user_id, shop_id):
    user_idx = user_mapping[user_id]
    shop_idx = shop_mapping[shop_id]
    prob = model.predict([np.array([user_idx]), np.array([shop_idx])])
    discount = '10%' if prob > 0.5 else '5%'
    return discount

# Example usage
user_id = 1
shop_id = 105
discount = get_personalized_discount(user_id, shop_id)
print(f"User {user_id} gets a {discount} discount at Shop {shop_id}")
