
import gym
import gym_game
import numpy as np
import random
def simulate():
    global epsilon, epsilon_decay
    for episode in range(MAX_EPISODES):

        state = env.reset()
        total_reward = 0

        for t in range(MAX_TRY):
            if(random.uniform(0, 1)<epsilon):
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])
            next_state, reward, done , _ = env.step(action)
            total_reward += reward
            q_value = q_table[state.astype(int)][action]
            best_q = np.max(q_table[next_state.astype(int)])

            q_table[state.astype(int)][action] = (1-learning_rate) * q_value + learning_rate * (reward + gamma * best_q)
            state = next_state
            env.render()
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i steps with total reward = %f." % (episode, t, total_reward))
                break


if __name__ == "__main__":
    env = gym.make("Tetris-v0")
    MAX_EPISODES = 10000
    MAX_TRY = 10000
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    gamma = 0.6
    num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    q_table = np.zeros(num_box + (env.action_space.n,))
    simulate()
