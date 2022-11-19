import random
import numpy as np
#from numpy.typing import NDArray
from typing import Iterable, List, Iterator, Tuple, NamedTuple

from config import *
from func import circle_generator
from input import make_input
from net import think



def deal_cards (HANDS: List[List[str]], KOLODA: List[str], TABLE: List[str], BITS: List[str]) -> Tuple[str,str]:
    flag = 1
    while flag:
        KOLODA.clear()
        KOLODA.extend ([card + NO_VISIBLE_CARD for card in FULL_KOLODA])
        random.shuffle(KOLODA)
        if KOLODA[-1][SLICE_RANK] == ACE:
            continue # если посл карат ТУЗ то пересдача
        else:
            flag = 0
        TABLE.clear()
        BITS.clear()
        for hand in HANDS:
            hand.clear()
            for x in range(6):
                hand.append(KOLODA.pop(0))
            hand.sort()
        KOLODA[-1] = KOLODA[-1].replace ('N', 'Y')
    if FLAG_PRINT:
        print('\ncards was dealed')
        print('KOLODA: ', KOLODA)
        print('last card: ', KOLODA[-1])
        print('TRUMP: ', KOLODA[-1][SLICE_MAST])
    return KOLODA[-1], KOLODA[-1][SLICE_MAST] # last_card, trump

def _find_min_trump (hand: List[str], TRUMP: str) -> int:
    min_trump = 100
    for c in hand:
        if c[SLICE_MAST] == TRUMP:
            rank = c[SLICE_RANK]
            indx_rank = RANK.index(rank)
            min_trump = min(min_trump, indx_rank)
    return min_trump

def first_attacker (HANDS: List[List[str]],TRUMP: str) -> int:
    list_min_trump = []
    for hand in HANDS:
        list_min_trump.append(_find_min_trump(hand,TRUMP))
    if min(list_min_trump) == 100: # ни у кого нет козыря
        return random.randint(0,len(HANDS)-1)
    else:
        return list_min_trump.index(min(list_min_trump))

def print_all (env: NamedTuple) -> None:
    if FLAG_PRINT:
        print("\nhands now are:")
        print('TRUMP = ', env.TRUMP)
        print('KOLODA = ', env.KOLODA, len(env.KOLODA))
        print('TABLE  = ', env.TABLE, len(env.TABLE))
        print('BITS   = ', env.BITS, len(env.BITS),'\n')
        for i, hand in enumerate(env.HANDS):
            print(f'hand[{i}] = {hand}', len(hand))

def list_hands_in_game (HANDS: List[List[str]]) -> List[int]:
    """ make list of hands with cards  """
    hands_in_game: List[int] = []
    for i,hand in enumerate(HANDS):
        if hand:
            hands_in_game.append (i)
    return hands_in_game

def change_attacker (old_hands: List[int], new_hands: List[int], result: bool) -> int:
    old_seq = circle_generator (old_hands)
    next(old_seq) #  = pass [0] old_attacker
    if not result:
        next(old_seq) #  = pass [1] old_defender if def was BAD
    for _ in range (len (old_hands)):
        a = next(old_seq)
        if a in new_hands:
            return a
    print('WTF')
    print('old_hands', old_hands)
    print('new_hands', new_hands)
    print('result', result)
    raise Exception('WTF')

def sort_hands_in_game (hands: List[int], attacker: int) -> None:
    while hands[0] != attacker:
        hands.append (hands.pop (0))

def count_cards_in_hands (HANDS: List[List[str]]) -> List[int]:
    """ count cards in all hands """
    count_list = []
    for hand in HANDS:
        count_list.append(len(hand))
    return count_list

def count_max_attacks (HANDS: List[List[str]], defender: int) -> int:
    """ count max attacks in round """
    count_list = count_cards_in_hands (HANDS)
    count_defender = count_list.pop(defender)
    return min(count_defender, sum(count_list))

def av_attack_card (hand: List[str],TABLE: List[str]) -> List[str]:
    av_cards = []
    assert len(TABLE) > 0, 'ERROR TABLE EMPTY !!!'
    table_ranks = { x[SLICE_RANK] for x in TABLE }
    for card in hand:
        if card[SLICE_RANK] in table_ranks:
            av_cards.append(card)
    if av_cards:
        assert len(av_cards[0]) == 4
    return av_cards

def av_defend_card (hand: List[str], TABLE: List[str], TRUMP: str) -> List[str]:
    assert len(TABLE) % 2 == 1, "перед защитой на столе дб нечетное кол карт"
    av_cards = []
    ct = TABLE[-1]
    ct_mast = ct[SLICE_MAST]
    ct_rank = ct[SLICE_RANK]
    for card in hand:
        if ct_mast == TRUMP:
            if card[SLICE_MAST] == TRUMP and int(card[SLICE_RANK]) > int(ct_rank):
                av_cards.append(card)
        else:
            if (card[SLICE_MAST] == ct_mast and int(card[SLICE_RANK]) > int(ct_rank)) or card[SLICE_MAST] == TRUMP:
                av_cards.append(card)
    return av_cards

def put_card_on_table (hand: List[str], ind_card: int, table: List[str]) -> None:
    ''' del card from hand, replace N to Y , put on TABLE '''
    table.append (hand.pop(ind_card)[SLICE_WO_VISIBLE] + VISIBLE_CARD)

def think_and_attack (id_hand: int, env: NamedTuple) -> None:
    # make input_vectior and convert to array
    input_array = make_input (id_hand, env)
    # находим мой атакующий мозг
    brain = env.BRAINS_ATTACK [id_hand] #
    # прогнать входной вектор через мозг 
    id_card, need_move = think (env.HANDS[id_hand], input_array, brain, activate=np.tanh) # индекс в фулл колоде и решение надо ли делать ход
    # делаем ход
    need_move = 1 if not len(env.TABLE) else need_move # если стол пуст надо делать ход в любом случае
    if need_move:
        for i,c in enumerate(env.HANDS[id_hand]):
            if c[SLICE_WO_VISIBLE] == FULL_KOLODA[id_card]:
                if FLAG_PRINT:
                    print(f'attack [{id_hand}] = ', env.HANDS[id_hand][i])
                put_card_on_table (env.HANDS[id_hand], i, env.TABLE)
                return None
        raise ValueError('WTF')
    else:
        if FLAG_PRINT:
            print(f'attack [{id_hand}] = no want attack')
    return None

def think_and_defend (id_hand: int, env: NamedTuple) -> None:
    # make input_vectior and convert to array
    input_array = make_input (id_hand, env)
    # находим мой атакующий мозг
    brain = env.BRAINS_DEFENSE [id_hand] #
    # прогнать входной вектор через мозг 
    id_card, need_move = think (env.HANDS[id_hand], input_array, brain, activate=np.tanh) # индекс в фулл колоде и решение надо ли делать ход
    # делаем ход
    need_move = 1 if (len(env.KOLODA) + len(env.HANDS[id_hand])) == 1 else need_move # если в колоде уже нет карт и у защитника послед карта то надо бить в любом случае
    if need_move:
        for i,c in enumerate(env.HANDS[id_hand]):
            if c[SLICE_WO_VISIBLE] == FULL_KOLODA[id_card]:
                put_card_on_table (env.HANDS[id_hand], i, env.TABLE)
                return None
        raise ValueError('WTF')
    return None

def play_round_by_net (list_id_hand: List[int], env: NamedTuple) -> bool:
    attacker, defender, count_attackers, seq_attackers = make_seq_attaclers (list_id_hand)
    if FLAG_PRINT:
        print('='*50)
        print('\n[attacker, defender] =', [attacker, defender])
        print(' hands_in_game       =', list_id_hand)
    max_attacks: int = count_max_attacks (env.HANDS, defender)
    count_no_move = 0 # counter for stop attack
    for _ in range(max_attacks):
        curr_attacker = next(seq_attackers)
        if not len(env.HANDS[curr_attacker]): # если атакер пуст то след атакер
            continue
        # attack
        if not len(env.TABLE): # if empty = first attack
            if len(env.HANDS[curr_attacker]) == 1: # если на руке одна карта просто кладем ее на стол
                if FLAG_PRINT:
                    print(f'attack [{curr_attacker}] = ', env.HANDS[curr_attacker][0])
                put_card_on_table (env.HANDS[curr_attacker], 0, env.TABLE)
            else: # если первый ход но карт на руке больше одной
                think_and_attack (curr_attacker, env)
        else: # стол не пуст
            availble_cards = av_attack_card (env.HANDS[curr_attacker],env.TABLE)
            if availble_cards:
                think_and_attack (curr_attacker, env)
        # defense
        if len(env.TABLE) % 2 == 0: # если четное, то атаки не было, НЕнадо защищаться
            count_no_move += 1
            if count_no_move >= count_attackers:
                break
        else: # была атака , надо защищаться
            availble_cards = av_defend_card (env.HANDS[defender], env.TABLE, env.TRUMP)
            if not availble_cards: # нечем бить
                if FLAG_PRINT:
                    print(f'defend [{defender}] = no def')
                return False
            else:
                think_and_defend (defender, env)
                if len(env.TABLE) % 2 == 1: # если решил не бить
                    if FLAG_PRINT:
                        print(f'defend [{defender}] = no want def')
                    return False
                else:
                    if FLAG_PRINT:
                        print(f'defend [{defender}] = ', env.TABLE[-1])
                    count_no_move = 0
    return True

def make_seq_attaclers (list_id_hand: List[int]) -> Tuple[int,int,int,Iterator]:
    attacker: int = list_id_hand[0]
    defender: int = list_id_hand[1]
    list_attackers: List[int] = list_id_hand.copy()
    list_attackers.remove(defender)
    seq_attackers: Iterator[int] = circle_generator (list_attackers)
    return attacker, defender, len(list_attackers), seq_attackers

def get_cards_from_koloda_attackers (hands: List[int], HANDS: List[List[str]], KOLODA: List[str]) -> None:
    """ добор карт из колоды после хода (attackers) """
    seq = hands.copy()
    seq.pop(1) # del defender
    for i in seq:
        while len(HANDS[i]) < 6 and len(KOLODA):
            HANDS[i].append(KOLODA.pop(0))

def get_cards_from_koloda_defender (hands: List[int], HANDS: List[List[str]], KOLODA: List[str]) -> None:
    """ добор карт из колоды после хода (defender) """
    while len(HANDS[hands[1]]) < 6 and len(KOLODA):
        HANDS[hands[1]].append(KOLODA.pop(0))



#def defend (hand: List[str],TABLE,TRUMP) -> bool:
#    av_cards = av_defend_card (hand,TABLE,TRUMP)
#    if av_cards:
#        rand_card = random.choice(av_cards)
#        indx = hand.index(rand_card)
#        print('attack   = ', TABLE[-1], 'defens = ', hand[indx])
#        #hand[indx] = hand[indx][SLICE_WO_VISIBLE] + VISIBLE_CARD
#        #TABLE.append(hand.pop(indx))
#        put_card_on_table (hand, indx, TABLE)
#        return True
#    else:
#        print('attack   = ', TABLE[-1], 'defens = NONE', av_cards)
#        return False

#def play_round (list_id_hand: List[int],HANDS,TABLE,TRUMP) -> bool:
#    """ return True if def is ok, False if def is bad """
#    attacker, defender, count_attackers, seq_attackers = \
#        make_seq_attaclers (list_id_hand)
#    print('\n[attacker, defender] =', [attacker, defender])
#    print(' hands_in_game       =', list_id_hand)
#    max_attacks: int = _count_max_attacks (HANDS, defender)
#    for _ in range(max_attacks):
#        if len(TABLE) == 0: # if first attack
#            availble_cards = HANDS[attacker]
#            attack (attacker,HANDS,TABLE) # add card to TABLE
#            if not defend (HANDS[defender],TABLE,TRUMP): # if def bad
#                return False
#        else: # not first attack
#            count_no_card = 0
#            for indx_hand in seq_attackers: # endless loop !!!
#                availble_cards = av_attack_card (HANDS[indx_hand],TABLE)
#                if availble_cards:
#                    attack (indx_hand,HANDS,TABLE) # add card to TABLE
#                    if not defend (HANDS[defender],TABLE,TRUMP): # if def bad
#                        return False
#                    else:
#                        break # OR break ??? (если break то )
#                else:
#                    count_no_card += 1
#                    if count_no_card >= count_attackers: #len(list_attackers):
#                        break
#    return True

#def attack (attacker: int,HANDS,TABLE) -> None:
#    hand = HANDS[attacker]
#    if not TABLE: # if TABLE is empty
#        if len(hand) == 1:
#            print(f'attack {attacker} = ', hand[0])
#            #hand[0] = hand[0][SLICE_WO_VISIBLE] + VISIBLE_CARD
#            #TABLE.append (hand.pop())
#            put_card_on_table (hand, 0, TABLE)
#        else:
#            rnd = random.randint(0,len(hand)-1)
#            print(f'attack {attacker} = ', hand[rnd])
#            #hand[rnd] = hand[rnd][SLICE_WO_VISIBLE] + VISIBLE_CARD
#            #TABLE.append (hand.pop(rnd))
#            put_card_on_table (hand, rnd, TABLE)
#    else:
#        table_rank = [] # list of RANK in TABLE
#        av_cards = [] # list of available cards to attack
#        for c in TABLE:
#            table_rank.append(c[SLICE_RANK])
#        for card in hand:
#            if card[SLICE_RANK] in table_rank:
#                av_cards.append (card)
#        rnd = random.randint(0,len(av_cards)-1)
#        print(f'attack {attacker} = ', av_cards[rnd])
#        indx = hand.index(av_cards[rnd])
#        #hand[indx] = hand[indx][SLICE_WO_VISIBLE] + VISIBLE_CARD
#        #TABLE.append (hand.pop(indx))
#        put_card_on_table (hand, indx, TABLE)

#def _check_posibility_attack (hand: List[str],TABLE) -> bool:
#    assert len(TABLE) > 0, 'ERROR TABLE EMPTY !!!'
#    table_rank: List[str] = [] # list of RANK in TABLE
#    for c in TABLE:
#        table_rank.append(c[SLICE_RANK])
#    for card in hand:
#        if card[SLICE_RANK] in table_rank:
#            return True
#    return False