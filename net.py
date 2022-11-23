import numpy as np
from typing import List, Callable, Tuple
from numpy.typing import NDArray
from numba import njit

from config import SIZE_OUT, PROB_MOVE, SHAPE_IN, BETA_TANH
from func import convert_listcard_to_binlist

#@njit
def tanh_with_beta (x):
    return np.tanh(BETA_TANH * x)

def init_brain (shape_list: List[tuple[int,int]]) -> List[List[NDArray]]:
    ''' create brain for player and init it by random float in [-1,1).
    brain is list of denses, dense is list [w, b] '''
    # brain = [dense1, dense2, ...]
    # dense = [w,b]
    # w = ndarray
    # b = ndarray
    rnd = np.random.default_rng()
    brain = []
    for shape in shape_list:
        brain.append([]) # add list for dense
        brain[-1].append((rnd.random(size=shape       , dtype='float32') * 2)-1) # matrix W random [-1,1)
        brain[-1].append((rnd.random(size=(shape[0],1), dtype='float32') * 2)-1) # matrix B random [-1,1)
    #assert np.array(brain, dtype=object).shape == (len(shape_list), 2)
    return brain

# с передачей функ активации
def think (av_cards: List[str], input_array: NDArray, brain: List[List[NDArray]], activate: Callable= np.tanh) -> Tuple[int,int]:
    ''' прогоняем входные данные через мозг и получаем индекс карты которой надо ходить и ответ ходить или нет '''
    W = 0
    B = 1
    assert input_array.shape == SHAPE_IN
    assert len(av_cards[0]) == 4 # must be with 'N' or 'Y'
    # av_cards - лист карт кот возможен ход
    # activate - actination function
    # brain[0] - это [W1, W2, ...]
    # brain[1] - это [B1, B2, ...]
    res = input_array.copy()
    for i in range(len(brain)-1): # сколько слоёв (пар W,B) кроме последнего
        res = activate (np.dot(brain[i][W], res) + brain[i][B]) # = tanh( W[i]*res + B[i])
    res = np.dot(brain[-1][W], res) + brain[-1][B] # посл слой считаем без функ активации
    # res сейчас это вектор с формой (37,1) , где каждое число от 0 до 1, те вероятность (первые 36 - карты, посл 1 - ходить/не ходить)
    # теперь оставляем вероятности только для карт кот есть в руке и которыми возможен ход.
    # умножая рез на бинарный массив (0 - нет карты, 1 - есть карта)
    res = res.reshape((SIZE_OUT,)) # shape -> (37,)
    prob_cards = res[:-1] # shape = (36,)
    prob_move  = res[-1] # float
    av_cards_arr = np.array (convert_listcard_to_binlist (av_cards), dtype=int) # shape=(36,)
    assert av_cards_arr.shape == (36,)
    mask = av_cards_arr.nonzero()[0] # индексы ненулевых элементов (tuple)
    max_ind = 0
    max_val = -1000.0
    for i in mask:
        if prob_cards[i] > max_val:
            max_ind = i
            max_val = prob_cards[i]
    
    return max_ind, int(prob_move > PROB_MOVE)

# с зашитой функ активации
#@njit
def think2 (av_cards: List[str], input_array: NDArray, brain: List[List[NDArray]]) -> Tuple[int,int]:
    ''' прогоняем входные данные через мозг и получаем индекс карты которой надо ходить и ответ ходить или нет '''
    W = 0
    B = 1
    assert input_array.shape == SHAPE_IN
    assert len(av_cards[0]) == 4 # must be with 'N' or 'Y'
    # av_cards - лист карт кот возможен ход
    # activate - actination function
    # brain[0] - это [W1, W2, ...]
    # brain[1] - это [B1, B2, ...]
    res = input_array.copy()
    for i in range(len(brain)-1): # сколько слоёв (пар W,B) кроме последнего
        res = tanh_with_beta (np.dot(brain[i][W], res) + brain[i][B]) # = tanh( W[i]*res + B[i])
    res = np.dot(brain[-1][W], res) + brain[-1][B] # посл слой считаем без функ активации
    # res сейчас это вектор с формой (37,1) , где каждое число от 0 до 1, те вероятность (первые 36 - карты, посл 1 - ходить/не ходить)
    # теперь оставляем вероятности только для карт кот есть в руке и которыми возможен ход.
    # умножая рез на бинарный массив (0 - нет карты, 1 - есть карта)
    res = res.reshape((SIZE_OUT,)) # shape -> (37,)
    prob_cards = res[:-1] # shape = (36,)
    prob_move  = res[-1] # float
    av_cards_arr = np.array (convert_listcard_to_binlist (av_cards), dtype=int) # shape=(36,)
    assert av_cards_arr.shape == (36,)
    mask = av_cards_arr.nonzero()[0] # индексы ненулевых элементов (tuple)
    max_ind = 0
    max_val = -1000.0
    for i in mask:
        if prob_cards[i] > max_val:
            max_ind = i
            max_val = prob_cards[i]
    
    return max_ind, int(prob_move > PROB_MOVE)

def print_brain (brain, print_dense = 0):
    for i,dense in enumerate (brain):
        if print_dense == i or print_dense == 0:
            print(f'dense[{i}]')
            print('W')
            print(dense[0])
            print('B')
            print(dense[1])
