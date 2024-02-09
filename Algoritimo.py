import random
import numpy as np
from utils import *


# Qtable no formato:
#           0  1  2  3  4   5   6   7   8   <- Posições no tabuleiro
# state_1
# state_2
# ....

class Algoritimo():

    def __init__(self, env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes):
        self.env = env
        self.q_table = np.zeros((3**9,9))
        self.alpha = alpha                  # Taxa de aprendizado , quão maior, maior valor se da ao aprendizado.
        self.gamma = gamma                  # O quão relevante são as ecompensas futuras em relação a atual 
        self.epsilon = epsilon              # Chance de escolha de ação aleatória 
        self.epsilon_min = epsilon_min
        self.epsilon_dec = epsilon_dec
        self.episodes = episodes
    
    def select_action(self, state):
        rv = random.uniform(0, 1)
        if rv < self.epsilon or len(get_available_slots(state['action_mask'])) == 9:
            # Random action  -Explore
            x = random.randint(0,8)
            while state['action_mask'][x] != 1:
                x = random.randint(0,8)
            return x
        
        # Exploit learned values
        # Impossibilitando ações não disponiveis , pegando o maior valor dentre as ações disponíveis
        qrow = self.q_table[hash_matrix(state , do_fill = True)].copy()
        for action, value in enumerate(qrow):
            if state['action_mask'][action] != 1:
                qrow[action] = np.nan
        return np.nanargmax(qrow)  