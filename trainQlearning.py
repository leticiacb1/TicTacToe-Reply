import gymnasium as gym
from pettingzoo.classic import tictactoe_v3
import random
from QLearning import QLearning


env = tictactoe_v3.env()
qlearn = QLearning(env, alpha=.7, gamma=.8, epsilon=.999, epsilon_min=0.05, epsilon_dec=0.9999999999, episodes=100000)
#q_table,r1  = qlearn.train('data/q-table-tictac.csv', 'results/actions')
q_table  = qlearn.train()