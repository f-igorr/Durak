import random
from typing import Iterable, List, Iterator, Tuple
from config import *
from func import circle_generator
from input import make_input
from net import think
import numpy as np


def deal_cards (HANDS, KOLODA, TABLE, BITS) -> Tuple[str,str]:
    flag = 1
    while flag:
        KOLODA.clear()
        KOLODA.extend ([x + y + NO_VISIBLE_CARD for x in MASTI for y in RANK])
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
        #KOLODA[-1] = KOLODA[-1][SLICE_WO_VISIBLE] + 'Y' # посл карту видят все
        KOLODA[-1] = KOLODA[-1].replace ('N', 'Y')
    print('\ncards was dealed')
    print('rest: ', KOLODA)
    print('last card: ', KOLODA[-1])
    print('TRUMP: ', KOLODA[-1][SLICE_MAST])
    return KOLODA[-1], KOLODA[-1][SLICE_MAST] # last_card, trump

def _find_min_trump (hand: List[str], TRUMP) -> int:
    min_trump = 100
    for c in hand:
        if c[SLICE_MAST] == TRUMP:
            rank = c[SLICE_RANK]
            indx_rank = RANK.index(rank)
            min_trump = min(min_trump, indx_rank)
    return min_trump

def first_attacker (HANDS,TRUMP) -> int:
    list_min_trump = []
    for hand in HANDS:
        list_min_trump.append(_find_min_trump(hand,TRUMP))
    if min(list_min_trump) == 100: # ни у кого нет козыря
        return random.randint(0,len(HANDS)-1)
    else:
        return list_min_trump.index(min(list_min_trump))

def print_all (HANDS,KOLODA,TABLE,BITS,TRUMP) -> None:
    print("\nhands now are:")
    print('TRUMP = ', TRUMP)
    print('KOLODA = ', KOLODA, len(KOLODA))
    print('TABLE  = ', TABLE, len(TABLE))
    print('BITS   = ', BITS, len(BITS))
    for i, hand in enumerate(HANDS):
        print(f'hand[{i}] = {hand}', len(hand))

def list_hands_in_game (HANDS) -> List[int]:
    """ make list of hands with cards  """
    hands_in_game: List[int] = []
    for i,hand in enumerate(HANDS):
        if hand:
            hands_in_game.append (i)
    return hands_in_game

def change_attacker (old_hands: List[int], new_hands: List[int], result: bool) -> int:
    # old_attacker = old_hands[0]
    old_seq = circle_generator (old_hands)
    next(old_seq) #  = pass [0] old_attacker
    if not result:
        next(old_seq) #  = pass [1] old_defender if def was BAD
    for _ in range (len (new_hands)):
        a = next(old_seq)
        if a in new_hands:
            return a
    print('WTF')
    raise Exception('WTF')

def sort_hands_in_game (hands: List[int], attacker: int) -> None:
    while hands[0] != attacker:
        hands.append (hands.pop (0))

def _count_cards_in_hands (HANDS) -> List[int]:
    """ count cards in all hands """
    count_list = []
    for hand in HANDS:
        count_list.append(len(hand))
    return count_list

def _count_max_attacks (HANDS, defender: int) -> int:
    """ count max attacks in round """
    count_list = _count_cards_in_hands (HANDS)
    count_defender = count_list.pop(defender)
    return min(count_defender, sum(count_list))

#def _check_posibility_attack (hand: List[str],TABLE) -> bool:
#    assert len(TABLE) > 0, 'ERROR TABLE EMPTY !!!'
#    table_rank: List[str] = [] # list of RANK in TABLE
#    for c in TABLE:
#        table_rank.append(c[SLICE_RANK])
#    for card in hand:
#        if card[SLICE_RANK] in table_rank:
#            return True
#    return False

def pos_attack_card (hand: List[str],TABLE) -> List[str]:
    res = []
    assert len(TABLE) > 0, 'ERROR TABLE EMPTY !!!'
    table_ranks = { x[SLICE_RANK] for x in TABLE }
    for card in hand:
        if card[SLICE_RANK] in table_ranks:
            res.append(card)
    return res

def attack (attacker: int,HANDS,TABLE) -> None:
    hand = HANDS[attacker]
    if not TABLE: # if TABLE is empty
        if len(hand) == 1:
            print(f'attack {attacker} = ', hand[0])
            hand[0] = hand[0][SLICE_WO_VISIBLE] + VISIBLE_CARD
            TABLE.append (hand.pop())
        else:
            rnd = random.randint(0,len(hand)-1)
            print(f'attack {attacker} = ', hand[rnd])
            hand[rnd] = hand[rnd][SLICE_WO_VISIBLE] + VISIBLE_CARD
            TABLE.append (hand.pop(rnd))
    else:
        table_rank = [] # list of RANK in TABLE
        av_cards = [] # list of available cards to attack
        for c in TABLE:
            table_rank.append(c[SLICE_RANK])
        for card in hand:
            if card[SLICE_RANK] in table_rank:
                av_cards.append (card)
        rnd = random.randint(0,len(av_cards)-1)
        print(f'attack {attacker} = ', av_cards[rnd])
        indx = hand.index(av_cards[rnd])
        hand[indx] = hand[indx][SLICE_WO_VISIBLE] + VISIBLE_CARD
        TABLE.append (hand.pop(indx))
        
def _cards_for_defend (hand: List[str],TABLE,TRUMP) -> List[str]:
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

def defend (hand: List[str],TABLE,TRUMP) -> bool:
    av_cards = _cards_for_defend (hand,TABLE,TRUMP)
    if av_cards:
        rand_card = random.choice(av_cards)
        indx = hand.index(rand_card)
        print('attack   = ', TABLE[-1], 'defens = ', hand[indx])
        hand[indx] = hand[indx][SLICE_WO_VISIBLE] + VISIBLE_CARD
        TABLE.append(hand.pop(indx))
        return True
    else:
        print('attack   = ', TABLE[-1], 'defens = NONE', av_cards)
        return False

def play_round (hands: List[int],HANDS,TABLE,TRUMP) -> bool:
    """ return True if def is ok, False if def is bad """
    attacker: int = hands[0]
    defender: int = hands[1]
    list_attackers: List[int] = hands.copy()
    list_attackers.remove(defender)
    seq_attackers: Iterator[int] = circle_generator (list_attackers)

    print('\n[attacker, defender] =', [attacker, defender])
    print(' hands_in_game       =', hands)

    max_attacks: int = _count_max_attacks (HANDS, defender)
    for _ in range(max_attacks):
        if len(TABLE) == 0: # if first attack
            availble_cards = HANDS[attacker]
            attack (attacker,HANDS,TABLE) # add card to TABLE
            if not defend (HANDS[defender],TABLE,TRUMP): # if def bad
                return False
        else: # not first attack
            count_no_card = 0
            for indx_hand in seq_attackers: # endless loop !!!
                availble_cards = pos_attack_card (HANDS[indx_hand],TABLE)
                if availble_cards:
                    attack (indx_hand,HANDS,TABLE) # add card to TABLE
                    if not defend (HANDS[defender],TABLE,TRUMP): # if def bad
                        return False
                    else:
                        break # OR break ??? (если break то )
                else:
                    count_no_card += 1
                    if count_no_card >= len(list_attackers):
                        break
    return True

def get_cards_from_koloda_attackers (hands: List[int],HANDS,KOLODA) -> None:
    """ добор карт из колоды после хода (attackers) """
    seq = hands.copy()
    seq.pop(1) # del defender
    for i in seq:
        while len(HANDS[i]) < 6 and len(KOLODA):
            HANDS[i].append(KOLODA.pop(0))

def get_cards_from_koloda_defender (hands: List[int],HANDS,KOLODA) -> None:
    """ добор карт из колоды после хода (defender) """
    while len(HANDS[hands[1]]) < 6 and len(KOLODA):
        HANDS[hands[1]].append(KOLODA.pop(0))

def attack_by_net (id, av_cards, HANDS, KOLODA, TABLE, BITS, LAST_CARD, TRUMP, BRAINS_ATTACK):
    # make input_vectior and convert to array
    input_array = make_input (id, HANDS,KOLODA, TABLE, BITS, LAST_CARD, TRUMP)
    # находим мой атакующий мозг
    brain = BRAINS_ATTACK [id] #
    # прогнать входной вектор через мозг 
    indx_card = think (av_cards, input_array, brain, activate=np.tanh)

    # ДОПИСАТЬ 
