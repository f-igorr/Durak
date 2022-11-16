import numpy as np
from typing import List
from numpy.typing import NDArray

rnd = np.random.default_rng()


# ширина слоя
SIZE_IN = 2  # входной слой
SIZE_D1 = 3  # 1-й скрытый слой
SIZE_D2 = 2  # 2-й скрытый слой
SIZE_OUT = 1 # выходной слой

# форма слоя
SHAPE_IN      = (SIZE_IN , 1) # (4,1)
SHAPE_DENSE_1 = (SIZE_D1 , SIZE_IN) # (20,4)
SHAPE_DENSE_2 = (SIZE_D2 , SIZE_D1) # (10,20)
SHAPE_OUT     = (SIZE_OUT, SIZE_D2) # (3,10)

count_brains = 4 # len(HANDS)
shape_list = [SHAPE_IN, SHAPE_DENSE_1, SHAPE_DENSE_2, SHAPE_OUT]

def init_list_brains (count_brains: int, shape_list: List[tuple[int,int]]) -> List[List[NDArray]]:
    res: List[List[NDArray]] = [[] for x in range(count_brains)]
    for br in res:
        for sh in shape_list:
            br.append((rnd.random(size=sh, dtype=float)*2)-1)
    return res

init_list_brains (4, shape_list)