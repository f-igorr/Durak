from typing import List


ACE = '14' # пересдаем если послед карта туз (14)
MASTI = ('D','H','C','S') # буби, черви, трефы, пики
RANK = ['06','07','08','09','10','11','12','13','14'] #('6','7','8','9','10','J','Q','K','A')
FULL_KOLODA = [x+y for x in MASTI for y in RANK]
NO_VISIBLE_CARD = 'N' # (N or Y) признак видели ли эту карту другие игроки (если не отбился, взял из колоды посл карту)
VISIBLE_CARD = 'Y'
LEN_BIN_QTY = 6 # кол-во цифр в кодировке количеств


SLICE_MAST = slice(1)
SLICE_RANK  = slice(1,3)
SLICE_WO_VISIBLE = slice(0,-1)

INDX_FIRST_MY_CARDS = 42 # wil be included to slice
INDX_LAST_MY_CARDS = 42 + 36 # will be not included to slice
SLICE_MY_CARDS = slice(INDX_FIRST_MY_CARDS, INDX_LAST_MY_CARDS)

LEN_INPT_VECTOR = 298 # длина входного вектора

# ПРАМЕТРЫ НЕЙРОСЕТИ
# ширина слоя
SIZE_IN = 2  # входной слой
SIZE_D1 = 3  # 1-й скрытый слой
SIZE_D2 = 2  # 2-й скрытый слой
SIZE_OUT = 1 # выходной слой

# форма слоя
SHAPE_IN      = (SIZE_IN , 1) # input data
SHAPE_DENSE_1 = (SIZE_D1 , SIZE_IN) # part of brain
SHAPE_DENSE_2 = (SIZE_D2 , SIZE_D1) # part of brain
SHAPE_OUT     = (SIZE_OUT, SIZE_D2) # part of brain