

# ==========  GAME  =======================

ACE = '14' # пересдаем если послед карта туз (14)
MASTI = ('C','D','H','S') # буби, черви, трефы, пики
RANK = ['06','07','08','09','10','11','12','13','14'] #('6','7','8','9','10','J','Q','K','A')
FULL_KOLODA = sorted([x+y for x in MASTI for y in RANK])
LEN_FULL_KOLODA = len(FULL_KOLODA)
NO_VISIBLE_CARD = 'N' # (N or Y) признак видели ли эту карту другие игроки (если не отбился, взял из колоды посл карту)
VISIBLE_CARD = 'Y'
LEN_BIN_QTY = 6 # кол-во цифр в кодировке количеств

SLICE_MAST = slice(1)
SLICE_RANK  = slice(1,3)
SLICE_WO_VISIBLE = slice(0,-1)

PROB_MOVE = 0.5 # если НС выдает больше 0,5 то делаем ход
MAX_LEN_GAME = 200 # макс кол-во ходов в игре (тк бывает зацикливоние)

LIMIT_GAMES = 10 # кол-во игр с одними мозгами

# ==========  NET  =======================

LEN_INPT_VECTOR = 298 # длина входного вектора

# ПРАМЕТРЫ НЕЙРОСЕТИ
# ширина слоя
SIZE_IN = LEN_INPT_VECTOR  # входной слой
SIZE_D1 = 10  # 1-й скрытый слой
SIZE_D2 = 10  # 2-й скрытый слой
SIZE_OUT = 37 # выходной слой 36 + 1 = 37 (+1 чтобы решать ходить/не ходить)
# форма слоя
SHAPE_IN      = (SIZE_IN , 1) # input data
SHAPE_DENSE_1 = (SIZE_D1 , SIZE_IN) # part of brain
SHAPE_DENSE_2 = (SIZE_D2 , SIZE_D1) # part of brain
SHAPE_OUT     = (SIZE_OUT, SIZE_D2) # part of brain
SHAPE_LIST_FOR_BRAINS = [SHAPE_DENSE_1, SHAPE_DENSE_2, SHAPE_OUT]


# ==========  OTHERS  =======================

FLAG_PRINT = 0

# ==========  GENETIKA  =======================
PERCENT_MUTATION = 0.01 # 5%
LIMIT_WEIGHT = 2.0 # +5/-5
ALFA = 0.5