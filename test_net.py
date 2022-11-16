import numpy as np
from typing import List, Callable
from numpy.typing import ArrayLike, NDArray



# ширина слоя
SIZE_IN = 4  # входной слой
SIZE_D1 = 3  # 1-й скрытый слой
SIZE_D2 = 2  # 2-й скрытый слой
SIZE_OUT = 2 # выходной слой

# форма слоя
SHAPE_IN      = (SIZE_IN , 1) # (4,1)
SHAPE_DENSE_1 = (SIZE_D1 , SIZE_IN) # (20,4)
SHAPE_DENSE_2 = (SIZE_D2 , SIZE_D1) # (10,20)
SHAPE_OUT     = (SIZE_OUT, SIZE_D2) # (3,10)

# входные данные
inp_list = [0,1,2,3]
inp_arr = np.array(inp_list).reshape(SHAPE_IN)
# значения весов
w_1   = np.arange(SIZE_D1 * SIZE_IN).reshape(SHAPE_DENSE_1)
b_1   = np.arange(SIZE_D1).reshape((SHAPE_DENSE_1[0],1))
w_2   = np.arange(SIZE_D2 * SIZE_D1).reshape(SHAPE_DENSE_2)
b_2   = np.arange(SIZE_D2).reshape((SHAPE_DENSE_2[0],1))
w_out = np.arange(SIZE_OUT * SIZE_D2).reshape(SHAPE_OUT)
b_out = np.arange(SIZE_OUT).reshape((SHAPE_OUT[0],1))


def test_dot (inp_arr):
    ''' test ONLY dot and plus (no activ func) '''
    res = inp_arr
    res = np.dot(w_1  , res) + b_1
    res = np.dot(w_2  , res) + b_2
    res = np.dot(w_out, res) + b_out

    print(res) # right res = [[519][1892]]

test_dot(inp_arr)

#======================================

def test_activ_func (x):
    return x

# входные данные
inp_list = [0,1,2,3]
inp_arr = np.array(inp_list).reshape(SHAPE_IN)
list_wb = [w_1, w_2, w_out, b_1, b_2, b_out]
activ_func = np.tanh

def net (input: NDArray, list_wb: List[NDArray], activ_func: Callable) -> None:
    w_1, w_2, w_out, b_1, b_2, b_out =  list_wb
    res = input
    res = activ_func(np.dot(w_1  , res) + b_1  )
    res = activ_func(np.dot(w_2  , res) + b_2  )
    res = activ_func(np.dot(w_out, res) + b_out)

    print(res)

net (inp_arr, list_wb, test_activ_func) # right res = [[519][1892]]
net (inp_arr, list_wb, np.tanh) # right res = [ [0.76159416] [0.99998747] ]