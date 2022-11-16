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
