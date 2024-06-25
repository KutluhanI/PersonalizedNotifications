import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def create_and_train_model():
    user_data = pd.read_csv('../data/user_data.csv')
    shop_data = pd.read_csv('../data/shop_data.csv')
    purchase_history = pd.read_csv('../data/purchase_history.csv')
    negative_samples = pd.read_csv('../data/negative_samples.csv')

    full_data = pd.concat([purchase_history, negative_samples])

    user_mapping = {user_id: i for i, user_id in enumerate(user_data['user_id'].unique())}
    shop_mapping = {shop_id: i for i, shop_id in enumerate(shop_data['shop_id'].unique())}

    full_data['user_id'] = full_data['user_id'].map(user_mapping)
    full_data['shop_id'] = full_data['shop_id'].map(shop_mapping)

    num_users = len(user_mapping)
    num_shops = len(shop_mapping)
    embedding_size = 50

    user_input = Input(shape=(1,), name='user_input')
    shop_input = Input(shape=(1,), name='shop_input')

    user_embedding = Embedding(input_dim=num_users, output_dim=embedding_size, name='user_embedding')(user_input)
    shop_embedding = Embedding(input_dim=num_shops, output_dim=embedding_size, name='shop_embedding')(shop_input)

    user_vector = Flatten(name='user_flatten')(user_embedding)
    shop_vector = Flatten(name='shop_flatten')(shop_embedding)

    concat = Concatenate()([user_vector, shop_vector])

    hidden = Dense(128, activation='relu')(concat)
    hidden = Dense(64, activation='relu')(hidden)
    output = Dense(1, activation='sigmoid')(hidden)

    model = Model(inputs=[user_input, shop_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['AUC'])

    user_input_data = full_data['user_id'].values
    shop_input_data = full_data['shop_id'].values
    labels = full_data['label'].values

    user_input_train, user_input_test, shop_input_train, shop_input_test, y_train, y_test = train_test_split(
        user_input_data, shop_input_data, labels, test_size=0.2, random_state=42)

    model.fit([user_input_train, shop_input_train], y_train, epochs=10, batch_size=32, validation_data=([user_input_test, shop_input_test], y_test))

    model.save('../models/personalized_discount_model.keras')

    y_pred = model.predict([user_input_test, shop_input_test])
    auc_score = roc_auc_score(y_test, y_pred)
    print(f"AUC Score: {auc_score}")

    return model, user_mapping, shop_mapping
