import gymnasium as gym
from pettingzoo.classic import tictactoe_v3
import random
from utils import *
from numpy import loadtxt


def play_random_agent(agent, obs , env):
    x = env.action_space(agent).sample()
    while obs['action_mask'][x] != 1:
        x = env.action_space(agent).sample()
    return x

def play_min_max_agent(obs):
    matrix = fill_matrix(obs)
    result = minMax(matrix,len(get_available_slots(obs['action_mask'])),True)
    keys = [k for k, v in positions.items() if v == [result[0],result[1]]]
    return int(keys[0])

def play_qlearning_agent(obs):
    if len(get_available_slots(obs['action_mask'])) == 9:
        return random.randint(0,8)
    qtable = loadtxt('data/q-table.csv', delimiter=',')
    qrow = qtable[hash_matrix(obs , do_fill = True)].copy()
    for action, value in enumerate(qrow):
        if obs['action_mask'][action] != 1:
            qrow[action] = np.nan
    return np.nanargmax(qrow)  

def minmax_agent_vs_qlearning():
    losts = 0
    wins = 0
    draws = 0
    for i in range(0,100):
        env = tictactoe_v3.env()
        env.reset()
        not_finish = True
        while not_finish:
            for agent in ['player_1','player_2']:
                observation, reward, termination, truncation, info = env.last() 
                if termination or truncation:
                    not_finish = False
                else:
                    if agent == 'player_1':
                        action = play_qlearning_agent(observation)  # this is where you would insert your policy/algorithm 
                        print(f'Q learning play: ',action)
                    else:
                        action = play_min_max_agent(observation) # TODO change
                        print(f'MinMax play: ',action)
                    env.step(action)
        if env.rewards['player_1'] == 1:
            wins+=1
        elif env.rewards['player_1'] == -1:
            print(fill_matrix(observation))
            losts+=1
        else:
            draws+=1
        print(env.rewards)
    print(f"Wins: {wins}\nLosts: {losts}\nDraw: {draws}")

    
if __name__ == "__main__":
    print("Wich game do you want to see/play?\n0-minmax_agent_vs_qlearning")
    ans = int(input("Answer: "))
    if ans == 0:
        print("Showing 100 games")
        minmax_agent_vs_qlearning()
    else:
        print("Bad Answer")
        
