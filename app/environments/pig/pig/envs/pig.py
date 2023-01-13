
import gym
import numpy as np
import random

import config

from stable_baselines import logger

from .classes import *

class PigEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(PigEnv, self).__init__()
        self.name = 'pig'
        self.manual = manual
        
        self.n_players = 3
        
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(0, 100, [1 + self.n_players])

        self.verbose = verbose

    score_to_win = 100
        
    @property
    def observation(self):
        obs = np.array([self.current_pot] + [self.players[(self.current_player_num + i) % self.n_players].score for i in range(self.n_players)])
        return obs

    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def step(self, action):
        reward = [0] * self.n_players
        done = False

        if action == 0: #hold
            self.players[self.current_player_num].score += self.current_pot
            self.current_player_num = (self.current_player_num + 1) % self.n_players
            self.current_pot = self.roll()
        else:
            cur_roll = self.roll()
            if cur_roll == 1:
                self.current_player_num = (self.current_player_num + 1) % self.n_players
                self.current_pot = self.roll()
            else:
                self.current_pot += cur_roll
                if self.current_pot + self.players[self.current_player_num].score >= self.score_to_win:
                    reward[self.current_player_num] = 1
                    done = True
        
        return self.observation, reward, done, {}

    def roll(self):
        return random.randint(1,6)

    def reset(self):
        self.players = []
        self.current_player_num = 0
        self.current_pot = self.roll()
        

        player_id = 1
        for p in range(self.n_players):
            self.players.append(Player(str(player_id)))
            player_id += 1

        return self.observation

    @property
    def legal_actions(self):
        return np.array([1,1])

    def render(self, mode='human', close=False):
        
        if close:
            return

        for p in self.players:
            logger.debug(f'\nPlayer {p.id}\'s points: {p.score}')

        logger.debug(f'\nCurrent pot: {self.current_pot}')

    def rules_move(self):
        action_probs = [0.01] * self.action_space.n
        if self.current_pot < 20:
            action_probs[1] = .99
        else:
            action_probs[0] = .99
        return action_probs
