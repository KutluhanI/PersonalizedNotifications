import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import gym
from gym import spaces

# Müşteri ve bildirim verilerini yükleme
def load_data():
    data_path = "data/mock_data.csv"
    df = pd.read_csv(data_path)
    response_data = "data/mock_response_data.csv"
    response_df = pd.read_csv(response_data)
    return df, response_df

# Çevre sınıfı oluşturma
class NotificationEnv(gym.Env):
    def __init__(self, customer_data, response_data):
        super(NotificationEnv, self).__init__()

        self.customer_data = customer_data
        self.response_data = response_data

        self.action_space = spaces.Discrete(3)  # 3 farklı bildirim türü
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)

        self.state = self.reset()

    def reset(self):
        self.current_step = 0
        self.current_customer = self.customer_data.sample(1)
        self.state = np.array([0.5])
        return self.state

    def step(self, action):
        reward = np.random.choice([1, -1], p=[0.7, 0.3])
        self.current_step += 1
        done = self.current_step > 10
        self.state = np.array([0.5])
        return self.state, reward, done, {}

    def render(self):
        pass

# DQN modelini oluşturma
def build_dqn_model(input_shape, action_space):
    model = tf.keras.Sequential()
    model.add(layers.Dense(24, input_shape=input_shape, activation="relu"))
    model.add(layers.Dense(24, activation="relu"))
    model.add(layers.Dense(action_space, activation="linear"))
    return model

# Ajan sınıfı
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = build_dqn_model((state_size,), action_size)
        self.model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = np.random.choice(self.memory, batch_size, replace=False)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

# Ana fonksiyon
if __name__ == "__main__":
    customer_data, response_data = load_data()
    env = NotificationEnv(customer_data, response_data)
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    episodes = 1000
    batch_size = 32

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
    agent.save("dqn_model_example.h5")
