
import gym
from tensorflow.python.keras.mixed_precision.experimental import policy
import gym_game
import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Convolution2D
from tensorflow.keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy

env = gym.make("Tetris-v0")
height, width = env.observation_space.shape
actions = env.action_space.n
def randomMove():
    episodes = 5
    for episode in range(episodes):
        state = env.reset()
        done = False
        score = 0
        t = 0
        while not done:
            t+=1
            state = env.render()
            action = random.choice([0,1,2,3])
            n_state, reward, done, _ = env.step(action)
            score+=reward
        print("Episode %d finished after %i steps with total reward = %f." % (episode, t, score))
    env.close()


def build_model(height,width,actions):
    model = Sequential()
    model.add(Convolution2D(8,(4,4), activation ='relu', input_shape = (3,height,width,1)))
    model.add(Convolution2D(16,(4,4), activation ='relu'))
    model.add(Convolution2D(16,(3,3), activation ='relu'))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model


def build_agent(model,actions):
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.2, nb_steps=10000)
    memory = SequentialMemory(limit=1000, window_length=3)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,enable_dueling_network=True, dueling_type='avg',
        nb_actions=actions, nb_steps_warmup=1000)
    return dqn

model = build_model(height,width,actions)
model.summary()
dqn = build_agent(model, actions)
dqn.compile(Adam(lr=1e-4))

dqn.fit(env, nb_steps=10000, visualize=False, verbose=2)


