from typing import List
from game import  deal_cards, first_attacker, print_all, list_hands_in_game, play_round,\
    get_cards_from_koloda_attackers, get_cards_from_koloda_defender, change_attacker, sort_hands_in_game
from config import * 
from input import make_input

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

# select attacker and defender first time
hands_in_game: List[int] = list_hands_in_game (HANDS)
attacker: int = first_attacker (HANDS,TRUMP)
sort_hands_in_game (hands_in_game, attacker)
defender: int = hands_in_game[1]

print('\nfirst [attacker, defender] =', [attacker, defender])
print('hands_in_game                =', hands_in_game)

while True:
    print_all(HANDS,KOLODA,TABLE,BITS,TRUMP)

    #input_for_NN = make_input(0, HANDS, KOLODA, TABLE, BITS,LAST_CARD,TRUMP) # НЕ ЗДЕСЬ !

    #input('press enter for continue')

    result_round = play_round (hands_in_game,HANDS,TABLE,TRUMP)
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
        print(f'GAME OVER. DURAK is hand_{new_hands_in_game[0]}')
        break
    elif len(new_hands_in_game) == 0:
        print('GAME OVER. DRAW !')
        break
    attacker = change_attacker (hands_in_game, new_hands_in_game, result_round)
    hands_in_game = new_hands_in_game
    sort_hands_in_game (hands_in_game, attacker)
    defender = hands_in_game[1]

print('\n==== FINAL REULT ========')
print_all(HANDS,KOLODA,TABLE,BITS,TRUMP)