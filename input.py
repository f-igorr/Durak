#import numpy as np
from typing import List
from func import convert_int_to_list_bin, convert_listcard_to_binlist, circle_gen_with_first, convert_mastcard_to_binlist

# кодируем входные данные для НС
# всё кодируем в 0 или 1

# DONE кол-во карт: на руках всех игроков, на столе, в отбое, в колоде
# DONE мои карты [0, 0 ,1 ...] лист из 36  0 или 1
# DONE известные карты каждого игрока [0, 0 ,1 ...] лист из 36  0 или 1
# DONE карты на столе 
# DONE карты в отбое
# послед карта в колоде
# козырь [0,0,1,0]

def make_input (my_indx: int, HANDS: List[List[str]], KOLODA: List[str], TABLE: List[str], BITS: List[str], LAST_CARD: str,TRUMP: str) -> List[int]:
    ''' формирование входных данных для мозга (НС) '''
    inpt = []
    indx_hands = range(len(HANDS))
    # кол-во карт : у меня, след игрок, след игрок, след игрок, ...
    # кодируем кол-во в лист бинарного представления числа
    circle_seq_ind_hands = circle_gen_with_first (indx_hands, my_indx) # круговая последов-ть индексов рук
    bin_qty_in_hands = []
    for _ in indx_hands:
        i = next(circle_seq_ind_hands)
        bin_qty_in_hands.extend (convert_int_to_list_bin (len(HANDS[i]))) #  6 = [0,0,0,1,1,0]
    # кол-во карт на столе, в отбое, в колоде
    bin_qty_table  = convert_int_to_list_bin (len(TABLE))
    bin_qty_bits   = convert_int_to_list_bin (len(BITS))
    bin_qty_koloda = convert_int_to_list_bin (len(KOLODA))
    # мои карты и известные карты каждого игрока
    circle_seq_ind_hands = circle_gen_with_first (indx_hands, my_indx) # круговая последов-ть индексов рук
    bin_hands = []
    for _ in indx_hands:
        i = next(circle_seq_ind_hands)
        if i == my_indx: # first is my hand, add all cards
            bin_hands.extend (convert_listcard_to_binlist (HANDS[i]))
        else: 
            visible_cards = [c for c in HANDS[i] if c[-1] == 'Y']
            bin_hands.extend (convert_listcard_to_binlist (visible_cards))
    # карты на столе 
    bin_table = convert_listcard_to_binlist (TABLE)
    # карты в отбое
    bin_bits = convert_listcard_to_binlist (BITS)
    # послед карта в колоде
    bin_last_card = convert_listcard_to_binlist ([LAST_CARD])
    # козырь
    bin_trump = convert_mastcard_to_binlist (TRUMP)

    inpt.extend (bin_qty_in_hands)
    inpt.extend (bin_qty_table)
    inpt.extend (bin_qty_bits)
    inpt.extend (bin_qty_koloda)
    inpt.extend (bin_hands)
    inpt.extend (bin_table)
    inpt.extend (bin_bits)
    inpt.extend (bin_last_card)
    inpt.extend (bin_trump)

    print('\n INPT \n', inpt)

    return inpt