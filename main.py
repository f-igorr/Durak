from collections import namedtuple
from typing import List

from game import  deal_cards, first_attacker, print_all, list_hands_in_game, play_round_by_net,\
    get_cards_from_koloda_attackers, get_cards_from_koloda_defender, change_attacker, sort_hands_in_game
from config import * 
from net import init_list_brains


count_round_max = 200

def main():
    # ============================================
    hand_0 : List[str] = []
    hand_1 : List[str] = []
    hand_2 : List[str] = []
    hand_3 : List[str] = []
    HANDS = [hand_0, hand_1, hand_2, hand_3]

    KOLODA: List[str] = [] # колода карт которые еще не в игре (не взяты игроками)
    TABLE : List[str] = [] # карты текущего хода
    BITS  : List[str] = [] # вышедшие карты 
    # ============================================
    # START GAME
    LAST_CARD, TRUMP = deal_cards (HANDS, KOLODA, TABLE, BITS)
    # create and init brains 
    BRAINS_ATTACK  = init_list_brains (len(HANDS), SHAPE_LIST_FOR_BRAINS)
    BRAINS_DEFENSE = init_list_brains (len(HANDS), SHAPE_LIST_FOR_BRAINS)

    # create namedTuple to pass all params together to functions
    env = namedtuple ('env', ['HANDS','KOLODA','TABLE','BITS','LAST_CARD','TRUMP','BRAINS_ATTACK','BRAINS_DEFENSE'])
    ENV = env( HANDS,KOLODA,TABLE,BITS,LAST_CARD,TRUMP,BRAINS_ATTACK,BRAINS_DEFENSE )

    # select attacker and defender first time
    hands_in_game: List[int] = list_hands_in_game (HANDS)
    attacker: int = first_attacker (HANDS,TRUMP)
    sort_hands_in_game (hands_in_game, attacker)
    defender: int = hands_in_game[1]

    if FLAG_PRINT:
        print('\nSTART GAME')
        print('FULL_KOLODA\n', FULL_KOLODA)
        print('\nfirst [attacker, defender] =', [attacker, defender])
        print('hands_in_game                =', hands_in_game)

    count_round = 0
    while True and count_round < count_round_max:
        count_round += 1
        #print_all (ENV) #(HANDS,KOLODA,TABLE,BITS,TRUMP)

        #input('press enter for continue')

        result_round = play_round_by_net (hands_in_game, ENV)

        get_cards_from_koloda_attackers (hands_in_game,HANDS,KOLODA)
        if result_round: # True (def OK)
            BITS.extend(TABLE)
            TABLE.clear()
            get_cards_from_koloda_defender(hands_in_game,HANDS,KOLODA)
        else: # False (def is bad)
            HANDS[defender].extend(TABLE)
            TABLE.clear()
        new_hands_in_game = list_hands_in_game (HANDS)
        # check for end game
        if len(new_hands_in_game) == 1:
            #print(f'GAME OVER. DURAK is hand_{new_hands_in_game[0]}')
            break
        elif len(new_hands_in_game) == 0:
            #print('GAME OVER. DRAW !')
            break
        attacker = change_attacker (hands_in_game, new_hands_in_game, result_round)
        hands_in_game = new_hands_in_game
        sort_hands_in_game (hands_in_game, attacker)
        defender = hands_in_game[1]
    if FLAG_PRINT:
        print('\n==== FINAL REULT ========')
        print('count_round = ', count_round)
        print_all(ENV)
    return count_round

count_list = []
for g in range(20000):
    print(g)
    count_list.append( main() )

max_less_limit = [c for c in count_list if c != count_round_max]

print('max < limit', max(max_less_limit))
print('abs max', max(count_list))
print('len all', len(count_list))
print('len max_less_limit', len(max_less_limit))

#print('\n==== FINAL REULT ========')
#print('count_round = ', count_round)
#print_all(ENV)