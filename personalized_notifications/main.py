from scripts.data_processing import load_and_process_data
from scripts.category_analysis import analyze_categories
from scripts.notification_sender import send_notifications
from scripts.drl_model import DQNAgent, NotificationEnv, load_data

if __name__ == "__main__":
    df = load_and_process_data()
    top_categories = analyze_categories(df)
    send_notifications(top_categories)
    
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
