from typing import List
from collections import namedtuple
import numpy as np

from config import SHAPE_LIST_FOR_BRAINS
from net import init_brain, print_brain
from game import set_games
from genetika import mutation, crossover, create_new_population

# cards 
KOLODA: List[str] = [] # колода карт которые еще не в игре (не взяты игроками)
TABLE : List[str] = [] # карты текущего хода
BITS  : List[str] = [] # вышедшие карты 
LAST_CARD: List[str] = []
TRUMP: List[str] = []

# list of hands
hand_0 : List[str] = []
hand_1 : List[str] = []
hand_2 : List[str] = []
hand_3 : List[str] = []
HANDS = [hand_0, hand_1, hand_2, hand_3]
LIST_LOST = [0 for h in HANDS] # лист подсчета дураков

# first inition brains
BRAINS_ATTACK  = [ init_brain (SHAPE_LIST_FOR_BRAINS) for x in HANDS]
BRAINS_DEFENSE = [ init_brain (SHAPE_LIST_FOR_BRAINS) for x in HANDS]
assert np.array(BRAINS_ATTACK, dtype=object).shape == ( len(HANDS), len(SHAPE_LIST_FOR_BRAINS), 2)

# brains for check learning
brains_attack_random  = [ init_brain (SHAPE_LIST_FOR_BRAINS) for x in HANDS]
brains_defense_random = [ init_brain (SHAPE_LIST_FOR_BRAINS) for x in HANDS]
assert np.array(brains_attack_random, dtype=object).shape == ( len(HANDS), len(SHAPE_LIST_FOR_BRAINS), 2)

# create namedTuple to pass all params together to functions
env = namedtuple ('env', ['HANDS','KOLODA','TABLE','BITS','LAST_CARD','TRUMP','BRAINS_ATTACK','BRAINS_DEFENSE','LIST_LOST'])
ENV       = env( HANDS,KOLODA,TABLE,BITS,LAST_CARD,TRUMP,BRAINS_ATTACK,BRAINS_DEFENSE,LIST_LOST )
env_check = env( HANDS,KOLODA,TABLE,BITS,LAST_CARD,TRUMP,brains_attack_random,brains_defense_random,LIST_LOST )

NUM_GENERATIONS = 10000 # кол-во циклов отбора

for num in range(NUM_GENERATIONS):
    if num == 0: # first generation
        pass
    else:
        pass
        create_new_population (ENV) # отбор. скрещ. мутация = новые игроки (новые мозги)
    LIST_LOST.clear()
    LIST_LOST.extend([0 for h in HANDS])
    #print('================================')
    #print('  GAME mode 1')
    set_games (ENV) # несколько игр с пост мозгами и разными раздачами карт = победители
    #print('result GAME mode 1', LIST_LOST)
    #print('\nGAME mode check')
    brains_attack_random.pop(-1)
    brains_attack_random.append(BRAINS_ATTACK[0])
    brains_defense_random.pop(-1)
    brains_defense_random.append(BRAINS_DEFENSE[0])
    LIST_LOST.clear()
    LIST_LOST.extend([0 for h in HANDS])
    set_games (env_check) 
    print(f'[{num}]', '  *******  ' * LIST_LOST[-1])

print('result GAME mode check', LIST_LOST)