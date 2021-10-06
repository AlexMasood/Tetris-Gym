import gym
from gym import spaces
import numpy as np
from .tetris import Tetris
import pygame
class CustomEnv(gym.Env):
    def __init__(self):
        self.tetris = Tetris()
        self.tetris.gameControl.update()
        self.action_space = spaces.Discrete(4)
        print(type(self.tetris.gameControl.getBoard().board))
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([10, 10, 10, 10, 10]), dtype=np.int)#self.tetris.gameControl.getBoard().board, dtype=np.ndarray)

    def reset(self):
        #del self.tetris
        self.tetris.gameControl.resetGameControl()
        self.tetris.gameControl.setupScreen()
        if(self.tetris.mode == 1):
            self.tetris.surface.fill((0,0,0))
            self.tetris.surface.blit(self.tetris.changeModeText, (0,0))
            pygame.display.flip()
        self.tetris.gameControl.update()
        obs = self.tetris.observe()
        return obs

    def step(self, action):
        self.tetris.action(action)
        obs = self.tetris.observe()
        reward = self.tetris.evaluate()
        done = self.tetris.gameControl.exitGame
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.tetris.view()