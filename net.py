import numpy as np
from typing import List, Callable, Tuple
from numpy.typing import NDArray

from config import SIZE_OUT, PROB_MOVE, SHAPE_IN
from func import convert_listcard_to_binlist


def init_list_brains (count_brains: int, shape_list: List[tuple[int,int]]) -> List[List[List[NDArray]]]:
    ''' create list of brains for each player and init it by random float in [-1,1).
    each brain is set of list [w, b] '''
    # res = [brain1, brain2, ...]
    # brain = [ws, bs]
    # ws = [w1, w2, w_out]
    # bs = [b1,b2,b_out]
    # w1, .. = ndarray
    # b1, .. = ndarray
    W = 0
    B = 1
    rnd = np.random.default_rng()
    res: List[List[List[NDArray]]] = [[[],[]] for x in range(count_brains)]
    for brain in res:
        for shape in shape_list:
            brain[W].append((rnd.random(size=shape   , dtype='float32') * 2)-1) # matrix W random [-1,1)
            brain[B].append((rnd.random(size=(shape[0],1), dtype='float32') * 2)-1) # matrix B random [-1,1)
    return res

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
    for i in range(len(brain[W])): # сколько пар W,B
        res = activate (np.dot(brain[W][i], res) + brain[B][i]) # = tanh( W[i]*res + B[i])
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