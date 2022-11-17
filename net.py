import numpy as np
from typing import List, Callable, Tuple
from numpy.typing import NDArray
from config import *
from func import convert_listcard_to_binlist


def init_list_brains (count_brains: int, shape_list: List[tuple[int,int]]) -> List[List[List[NDArray]]]:
    ''' create list of brains for each player and init it by random float in [-1,1].
    each brain is set of list [w, b] '''
    # res = [brain1, brain2, ...]
    # brain = [ws, bs]
    # ws = [w1, w2, w_out]
    # bs = [b1,b2,b_out]
    # w1, .. = ndarray
    # b1, .. = ndarray
    rnd = np.random.default_rng()
    res: List[List[List[NDArray]]] = [[[],[]] for x in range(count_brains)]
    for brain in res:
        for shape in shape_list:
            brain[0].append((rnd.random(size=shape   , dtype='float32') * 2)-1) # matrix W random [-1,1]
            brain[1].append((rnd.random(size=shape[0], dtype='float32') * 2)-1) # matrix B random [-1,1]
    return res

def think (av_cards: List[str], input_array: NDArray, brain: List[List[NDArray]], activate: Callable= np.tanh) -> Tuple[int,int]:
    ''' прогоняем входные данные через мозг и получаем индекс карты которой надо ходить и ответ ходить или нет '''
    # av_cards - лист карт кот возможен ход
    assert len(av_cards[0]) == 4 # must be with 'N' or 'Y'
    # activate - actination function
    # brain[0] - это W1, W2, ...
    # brain[1] - это B1, B2, ...
    res = input_array.copy()
    for i in range(len(brain[0])): # сколько пар W,B
        res = activate (np.dot(brain[0][i], res) + brain[1][i]) # = tanh( W[i]*res + B[i])
    # res сейчас это вектор с формой (37,1) , где каждое число от 0 до 1, те вероятность (первые 36 - карты, посл 1 - ходить/не ходить)
    # теперь оставляем вероятности только для карт кот есть в руке и которыми возможен ход.
    # умножая рез на бинарный массив (0 - нет карты, 1 - есть карта)
    res = res.reshape((SIZE_OUT,)) # shape -> (37,)
    cards = res[:-1] # shape = (36,)
    move  = res[-1] # float
    av_cards_arr = np.array (convert_listcard_to_binlist (av_cards), dtype=int) # shape=(36,)
    prob_cards = cards * av_cards_arr # shape(36,) = shape(36,)*shape(36,)  #dont use np.dot
    return prob_cards.argmax(), int(move > PROB_MOVE)