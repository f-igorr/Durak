from copy import deepcopy
import numpy as np
from typing import List, NamedTuple
from numpy.typing import NDArray

from config import PERCENT_MUTATION, LIMIT_WEIGHT, ALFA


#def crossover (first: List[List[NDArray]], second: List[List[NDArray]]) -> tuple[List[List[NDArray]], List[List[NDArray]]]:
#    '''  '''
#    rnd = np.random.default_rng()
#    for f_dense,s_dense in zip(first, second): # denses
#        for f_arr, s_arr in zip(f_dense,s_dense): 
#            f_flat_arr = f_arr.reshape(-1)
#            s_flat_arr = s_arr.reshape(-1)
#            assert len(f_flat_arr) == len(s_flat_arr)
#            diff_arr = f_flat_arr - s_flat_arr
#            lim_1 = f_flat_arr - ALFA * diff_arr
#            lim_2 = s_flat_arr + ALFA * diff_arr
#            lim_min = np.minimum(lim_1, lim_2)
#            lim_max = np.maximum(lim_1, lim_2)
#            rnd_arr_1 = rnd.uniform (low=lim_min, high=lim_max)
#            rnd_arr_2 = rnd.uniform (low=lim_min, high=lim_max)


def crossover (first: List[List[NDArray]], second: List[List[NDArray]]) -> None:
    ''' crossover 2 brains: first and second.  '''
    rnd = np.random.default_rng()
    for f_dense,s_dense in zip(first, second): # denses
        for f_arr, s_arr in zip(f_dense,s_dense): 
            diff_arr = f_arr - s_arr
            lim_1 = f_arr - ALFA * diff_arr
            lim_2 = s_arr + ALFA * diff_arr
            lim_min = np.minimum(lim_1, lim_2)
            lim_max = np.maximum(lim_1, lim_2)
            f_arr[:] = rnd.uniform (low=lim_min, high=lim_max)
            s_arr[:] = rnd.uniform (low=lim_min, high=lim_max)
    return None


def mutation (brain: List[List[NDArray]]) -> None:
    ''' в каждом слое замена нескольких весов на случ знач '''
    rnd = np.random.default_rng()
    for dense in brain: # denses
        for arr in dense: 
            iter_by_arr = arr.flat # итератор по одномерному массиву
            len_arr = len(iter_by_arr) # длина уплощенного массива
            num_mut = 1 + int(len_arr * PERCENT_MUTATION) # кол-во мутирующих элементов в данном массиве
            ind_mut_item = rnd.integers(low=0, high=len_arr-1, size=num_mut) # массив случ индексов мут элементов
            for ind in ind_mut_item:
                #iter_by_arr[ind] = np.random.triangular(-LIMIT_WEIGHT, iter_by_arr[ind], LIMIT_WEIGHT) # замена веса на случ знач
                iter_by_arr[ind] = rnd.normal( iter_by_arr[ind], LIMIT_WEIGHT) # замена веса на случ знач
    return None


def create_new_population (env: NamedTuple):
    ''' создание новой популяции (для 4-х игроков).
    берем два лучших игрока.
    скрещиваем их, получаем 2 потомка.
    мутируем 1-го.
    берем 1-го без изменений  
    итог = [first, mut_first, cross_first_sec, cross_first_sec]'''
    # находим 2-х лучших
    copy_res = env.LIST_LOST.copy()
    ind_first = copy_res.index(min(copy_res))
    copy_res.pop(ind_first)
    ind_second = copy_res.index(min(copy_res))
    # save first and second
    first_att  = deepcopy (env.BRAINS_ATTACK [ind_first])
    first_def  = deepcopy (env.BRAINS_DEFENSE[ind_first])
    second_att = deepcopy (env.BRAINS_ATTACK [ind_second])
    second_def = deepcopy (env.BRAINS_DEFENSE[ind_second])
    # clear BRAINS_ATTACK and BRAINS_DEFENSE
    env.BRAINS_ATTACK.clear()
    env.BRAINS_DEFENSE.clear()
    # save first in brains (it will be [first])
    env.BRAINS_ATTACK.append (deepcopy(first_att)) 
    env.BRAINS_DEFENSE.append(deepcopy(first_def))
    # save first again and mutation it (it will be [first, first_mut])
    env.BRAINS_ATTACK.append (deepcopy(first_att))
    env.BRAINS_DEFENSE.append(deepcopy(first_def))
    mutation ( env.BRAINS_ATTACK[-1] )
    mutation ( env.BRAINS_DEFENSE[-1])
    # crossover first and second (it will be [first, first_mut, child_1, child_2])
    env.BRAINS_ATTACK.append (deepcopy(first_att)) 
    env.BRAINS_DEFENSE.append(deepcopy(first_def))
    env.BRAINS_ATTACK.append (deepcopy(second_att)) 
    env.BRAINS_DEFENSE.append(deepcopy(second_def))
    crossover (env.BRAINS_ATTACK [-2], env.BRAINS_ATTACK [-1])
    crossover (env.BRAINS_DEFENSE[-2], env.BRAINS_DEFENSE[-1])
