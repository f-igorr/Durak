from typing import List, NamedTuple
from func import convert_int_to_list_bin, convert_listcard_to_binlist, circle_gen_with_first, convert_mastcard_to_binlist
from config import *
import numpy as np
from numpy.typing import NDArray

# кодируем входные данные для НС
# всё кодируем в 0 или 1

# DONE кол-во карт: на руках всех игроков, на столе, в отбое, в колоде
# DONE мои карты [0, 0 ,1 ...] лист из 36  0 или 1
# DONE известные карты каждого игрока [0, 0 ,1 ...] лист из 36  0 или 1
# DONE карты на столе 
# DONE карты в отбое
# послед карта в колоде
# козырь [0,0,1,0]

# входной вектор: длина 298 
# кол-во карт у всех игроков : длина =  6 (кол-во на руке) * 4 (игорков) = 24 
# кол-во карт на столе: длина = 6 * 1 = 6
# кол-во карт в отбое: длина = 6 * 1 = 6
# кол-во карт в ост колоде: длина = 6 * 1 = 6
# мои карты и известные карты игроков: длина = 36 * 4 = 144
# карты на столе: длина = 36 * 1 = 36
# карты в отбое: длина = 36 * 1 = 36
# последняя карта в колоде: длина = 36 * 1 = 36
# масть козырей: длина = 4 * 1 = 4


# ДОБАВИТЬ В ВХ ВЕКТОР ЛИСТ МОИХ КАРТ , КОТРЫМИ ВОЗМОЖЕН ХОД ?????



#def make_input (my_indx: int, HANDS: List[List[str]], KOLODA: List[str], TABLE: List[str], BITS: List[str], LAST_CARD: str,TRUMP: str) -> NDArray:
def make_input (my_indx: int, env: NamedTuple) -> NDArray:
    ''' формирование входных данных для мозга (НС) '''
    inpt = []
    indx_hands = range(len(env.HANDS))
    # кол-во карт : у меня, след игрок, след игрок, след игрок, ...
    # кодируем кол-во в лист бинарного представления числа
    circle_seq_ind_hands = circle_gen_with_first (indx_hands, my_indx) # круговая последов-ть индексов рук
    bin_qty_in_hands = []
    for _ in indx_hands:
        i = next(circle_seq_ind_hands)
        bin_qty_in_hands.extend (convert_int_to_list_bin (len(env.HANDS[i]))) #  6 = [0,0,0,1,1,0]
    # кол-во карт на столе, в отбое, в колоде
    bin_qty_table  = convert_int_to_list_bin (len(env.TABLE))
    bin_qty_bits   = convert_int_to_list_bin (len(env.BITS))
    bin_qty_koloda = convert_int_to_list_bin (len(env.KOLODA))
    # мои карты и известные карты каждого игрока
    circle_seq_ind_hands = circle_gen_with_first (indx_hands, my_indx) # круговая последов-ть индексов рук
    bin_hands = []
    for _ in indx_hands:
        i = next(circle_seq_ind_hands)
        if i == my_indx: # first is my hand, add all cards
            bin_hands.extend (convert_listcard_to_binlist (env.HANDS[i]))
        else: 
            visible_cards = [c for c in env.HANDS[i] if c[-1] == 'Y']
            bin_hands.extend (convert_listcard_to_binlist (visible_cards))
    # карты на столе 
    bin_table = convert_listcard_to_binlist (env.TABLE)
    # карты в отбое
    bin_bits = convert_listcard_to_binlist (env.BITS)
    # послед карта в колоде
    bin_last_card = convert_listcard_to_binlist ([env.LAST_CARD])
    # козырь
    bin_trump = convert_mastcard_to_binlist (env.TRUMP)

    inpt.extend (bin_qty_in_hands)
    inpt.extend (bin_qty_table)
    inpt.extend (bin_qty_bits)
    inpt.extend (bin_qty_koloda)
    #assert len(inpt) == (len(HANDS) + 3) * LEN_BIN_QTY # 42
    inpt.extend (bin_hands)
    #assert len(inpt) == (len(HANDS) + 3) * LEN_BIN_QTY + len(HANDS) * 36 # 42+144=186
    inpt.extend (bin_table)
    inpt.extend (bin_bits)
    inpt.extend (bin_last_card)
    inpt.extend (bin_trump)

    assert len(inpt) == LEN_INPT_VECTOR

    #print('\n INPT \n', inpt)

    return np.array(inpt, dtype=int).reshape(SHAPE_IN)