import numpy as np
import random
from numpy import savetxt
import sys
from Algoritimo import Algoritimo
from tictac import *
from utils import *
from pettingzoo.classic import tictactoe_v3
from apply_action import apply_action

class QLearning(Algoritimo):

    def __init__(self, env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes):
          super().__init__(env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes)

    def train(self):
        actions_per_episode = []
        reward_per_episode = []
        reward_list = []
        rewards = 0
        wins,draws,losts = 0,0,0
        for i in range(1, self.episodes+1):
            self.env.reset()
            state = self.env.last()[0]
            done, termination, truncation = False, False, False
            turn = 1
            while not done:
                if termination or truncation:
                    done = True
                    reward_list.append(rewards)
                else:
                    # Escolhe uma ação
                    if turn == 1:
                        action = self.select_action(state)     
                        self.env.step(action)
                        next_state, reward, termination, truncation, info = self.env.last()
                        old_value = self.q_table[hash_matrix(state , do_fill =True), action]               # Valor da ação escolhida no estado atual 
                        next_max_action = np.max(self.q_table[hash_matrix(reverse_state(next_state), do_fill=True)]) # Melhor valor do estado futuro
                        if reward == 0 and termination:#draws
                            reward = 5
                            draws+=1
                        if reward != 0 and termination:#wins
                            reward = 10
                            wins+=1
                        new_value = old_value + self.alpha*(reward + self.gamma*next_max_action - old_value)          
                        self.q_table[hash_matrix(state, do_fill =True), action] = new_value
                        last_action = action
                        last_state = state
                        state = next_state
                        # Decaimento de epsilon:
                        if self.epsilon > self.epsilon_min:
                            self.epsilon = self.epsilon * self.epsilon_dec
                    else:
                        action = play_random_agent('player_2',state, self.env)
                        self.env.step(action)
                        next_state, reward, termination, truncation, info = self.env.last()
                        if (termination): #losts  
                            losts+=1
                            reward = -10
                            self.q_table[hash_matrix(last_state, do_fill =True), last_action] = reward
                        state = next_state
                    rewards+=reward
                    turn = -turn

            if i % 10 == 0:
                sys.stdout.write("  > Episodes: " + str(i) +'\r')
                sys.stdout.flush()
                pass
        print(f"\nWins rate: {100*wins/self.episodes}\nDraws: {100*draws/self.episodes}\nLosts: {100*losts/self.episodes}")
        savetxt('data/q-table.csv', self.q_table, delimiter=',')
        better_plotactions( 'Tictac', reward_list)
        return self.q_table