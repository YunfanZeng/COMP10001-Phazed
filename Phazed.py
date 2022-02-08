from itertools import combinations
from copy import deepcopy
from collections import defaultdict

# Q1
def colour_match(cards, accum=False):
    ''' Takes a list of cards and boolean accum to see if all cards belong to
    a colour. When accum is true, A is checked for colour, otherwise it is a
    wild card '''
    
    colour = None
    for card in cards:
        # If colour check isnt for accum, wildcards can be skipped
        if not accum:
            if card[0] == "A":
                continue
                
        # Sets the colour of the hand once
        if not colour:
            if card[1] in ["H", "D"]:
                colour = "R"
            else: 
                colour = "B"
        
        # Check if all other cards obey the set colour
        if colour == "R" and card[1] in ["S", "C"]:
            return False
        elif colour == "B" and card[1] in ["H", "D"]:
            return False
        else:
            continue
    return True

def set_checker(cards, set_dict, wild_cards, length):
    ''' Takes a list of cards, a dictionary (sorted by suit or value), a int of
    wild cards and length to check if cards belong in a suit or value set '''
    
    
    if len(cards) == length:
        for sets in set_dict.items():
            # If all cards are in set
            if len(sets[1]) == length:
                return True

            # If there are atleast two cards and enough wildcards 
            elif len(sets[1]) >= 2:
                if len(sets[1]) + wild_cards >= length:
                    return True
                
def check_sequence(value_list):
    ''' Takes a list value_list which consist of only the value of a card '''
    
    consec_a = 0
    nat_cards = 0
    start = 0

    for num in value_list:
        # Reset psuedo value if loops past king
        if start == 14:
            try:
                val = 1
                consec_a = 0

            except NameError:
                pass

        # Changes letter values to integers
        if num in ["0", "J", "Q", "K"]:
            for i in range(4):
                if num == ["0", "J", "Q", "K"][i]:
                    num = 10 + i 
                    break

        # If A occurs, skip a value 
        if num == "A":
            consec_a += 1
            start += 1
            continue

        # Try to define the current value, if it doesnt exist, initalise it
        try:
            val

        except NameError:
            # Initalise value and resets conseq_a count
            val = int(num)
            start = int(num) + 1
            consec_a = 0
            nat_cards += 1
            continue

        # Checks if the new value is in sequence, taking into account A's
        if int(val) + 1 + consec_a == int(num):
            val = num
            consec_a = 0
            start += 1
            nat_cards += 1
            continue

        else:
            return False

    # If atleast two natural cards are present, returns True
    if nat_cards < 2:
        return False
    else:
        return True   

def count_cards(card_set):
    ''' Takes input list card set and counts the numbers ''' 
    
    sum_num = 0
    for cards in card_set:
        num = cards[0]
        # Changes letter cards to integers and adds their values
        if num != "A":
            if num in ["0", "J", "Q", "K"]:
                for i in range(4):
                    if num == ["0", "J", "Q", "K"][i]:
                        num = 10 + i 
                        break
                        
            sum_num += int(num)
        else:
            sum_num += 1
    return sum_num

def phazed_group_type(group):
    ''' Takes input list group containing cards in the form "XY"
    and determines its group phase type '''
    
    cards = group
    wild_cards = 0
    
    phaze_groups = []
    value_list = []
    
    value_dict = defaultdict(list)
    suit_dict = defaultdict(list)
    
    # Arranging cards into lists with keys for values and suits
    for card in cards:
        if card[0] != "A":
            value_dict[card[0]].append(card)
            suit_dict[card[1]].append(card)
            
        else:
            wild_cards += 1 

    for card in cards:
        value_list.append(card[0])
    
    # Phaze 1 set of 3 with the same value
    if len(cards) == 3:
        if set_checker(cards, value_dict, wild_cards, len(cards)):
            phaze_groups.append(1) 

    # Phaze 2 set of 7 with the same suit
    if len(cards) == 7:
        if set_checker(cards, suit_dict, wild_cards, len(cards)):
            phaze_groups.append(2)
        
    # Phaze 3 set of 4 with the same value
    if len(cards) == 4:
        if set_checker(cards, value_dict, wild_cards, len(cards)):  
            phaze_groups.append(3)
            
    # Phaze 4 run of 8
    if len(cards) == 8:
        if check_sequence(value_list):
            phaze_groups.append(4)
            
    # Phase 5 run of 4 with the same colour
    if len(cards) == 4:
        if colour_match(cards):
            if check_sequence(value_list):
                phaze_groups.append(5)
    
    # Phase 6 acccumulation of 34
    if count_cards(cards) == 34:
        phaze_groups.append(6)
            
    # Phase 7 accumulation of 34 with the same colour
    if colour_match(cards):  
        if count_cards(cards) == 34:
            phaze_groups.append(7)
            
    return sorted(phaze_groups)

# Q2
def phazed_phase_type(phase):
    ''' Takes input list of lists phase containing 1-2 sets of cards
    and determines its phase type '''
    
    phase_type = []
    phases = []
    poss_group = [0, 0, 0, 0, 0, 0, 0]
    
    # Finds phase group of all lists
    for lists in phase:
        phase_type.append(phazed_group_type(lists))
        
    # Maps amount of times phase groups appear in line with Q1
    for group in phase_type:
        for combination in group:
            for i in range(1, 8):
                if combination == i:
                    poss_group[i - 1] += 1
                    
        # Find phases 1 - 7 in order
        if poss_group[0] == 2:
            phases.append(1)

        if poss_group[1] == 1:
            phases.append(2)
        
        if poss_group[5]== 2:
            phases.append(3)

        if poss_group[2] == 2:
            phases.append(4)

        if poss_group[3] == 1:
            phases.append(5)

        if poss_group[6] == 2:
            phases.append(6)

        if poss_group[4] == 1:
            if poss_group[2] == 1:
                phases.append(7)

    return sorted(phases)
    
# Q3
def phazed_is_valid_play(play, player_id, table, turn_history, phase_status, 
                         hand, discard):
    ''' Takes game information to determine if a move made by the player is 
    valid. Information from the game environment are used to determine if the
    players play (a 2-tuple describing their action and content) abides by the
    rules '''
    
    valid_play = True
    curr_player_turn = False
    curr_player_phase = phase_status[player_id]
    
    if turn_history:
        if turn_history[-1][0] == player_id:
            curr_player_turn = True
        
    # Validity check for pick up from deck and discard
    if play[0] == 1 or play[0] == 2:
        if curr_player_turn:
            return False
        
        # Check if card in discard
        if play[0] == 2:
            if not discard:
                return False
            
            # Check if card is in discard
            elif play[1] != discard:
                return False
                
    # Check for valid phases
    elif play[0] == 3:
        declared_phase = play[1][1]
        declared_phase_type = play[1][0]
        
        # Check if phase is valid
        if declared_phase_type not in phazed_phase_type(declared_phase):
            return False
            
        # Check if declared phase is the same as played phase
        if declared_phase_type != curr_player_phase + 1:
            return False
            
        # Check if they have drawn a card
        if not curr_player_turn:
            return False
    
        # Check if phase already played
        if table[player_id][0]:
            return False
        
        # Check if cards are in hand
        hand_copy = hand.copy()
        for lists in play[1][1]:
            for card in lists:
                if card in hand_copy:
                    hand_copy.remove(card)       
                else:
                    return False
    
    # Check if play onto phase is valid
    elif play[0] == 4:
        table_phase = table[play[1][1][0]][0]      # Phase of player table
        group = play[1][1][1]                      # Group index
        table_cards = table[play[1][1][0]][1]      # Sets of cards on table
        index_pos = play[1][1][2]                  # Index in group
        card = play[1][0]                          # Declared card
        table_cards_copy = table_cards.copy()
        
        # Check if player has drawn
        if not curr_player_turn:
            return False
        
        # Check if phase has been played
        if not table[player_id][0]:
            return False
        
        # Check if card in hand
        if card not in hand:
            return False


        
        # Check if index exists and if it is played at the correct index
        try:
            if index_pos not in [0, len(table_cards[group])]:
                return False
        except:
            return False
        
        # For runs and sets, remove a value and insert card to check validity
        if table_phase in [1, 2, 4, 5, 7]:
            if index_pos == 0:
                table_cards_copy[group].pop(-1)
                table_cards_copy[group].insert(0, card)
            else:
                table_cards_copy[group].pop(0)
                table_cards_copy[group].append(card)

            find_group = phazed_phase_type(table_cards_copy)
            
            # Check if returned phaze type is the same as current table phase
            if card[0] != "A":
                if not find_group:
                    return False

                elif table_phase not in find_group:
                    return False
            else:
                return True
                
        # Check if the card played is less than or equal to next fibb addition
        elif table_phase in [3, 6]:
            sum_of_orig = count_cards(table_cards[group])  
            table_cards_copy[group].append(card)
            sum_of_accum = count_cards(table_cards_copy[group])
            fibb = [34, 21, 13, 8, 5, 3, 2, 1, 1]
            orig_seq = True
            i = 0
            total = 0
            
            if table_phase == 6:
                # True for colour match to account for ace colour
                if not colour_match(table_cards_copy, True):
                    return False

            # Finds the original accum value (34, 55 etc.)
            while orig_seq:
                if fibb[i] + total != sum_of_orig:
                    total += fibb[i]
                    i += 1
                    
                else:
                    total = fibb[i] + total
                    orig_seq = False
            
            # Check if value between both accum values (i.e 34 < sum <= 55)
            if not total < sum_of_accum <= total + fibb[i + 1]:
                return False
            
            # Check if you have enough cards in hand
            elif sum_of_accum != total + fibb[i + 1] and len(hand) < 2:
                return False
            
    # Check if valid discard
    elif play[0] == 5:
        poss_accum = [34, 55, 68, 76, 81, 84, 86, 87, 88]
        
        # Check if discard before draw
        if not curr_player_turn:
            return False
        
        # Check if discard in hand
        if play[1] not in hand:
            return False

        # Check if all accum on table are valid at discard
        for player_table in table:
            if player_table[0] in [3, 6]:
                for sets in player_table[1]:
                    if count_cards(sets) not in poss_accum:
                        return False

    return valid_play

def accum_check(value_hand, num_to_letter, value_dict, wild_list, 
                colour_dict, colour=False):
    
    ''' Check if a hand is an accum. Takes inputs value_hand (Only values,
    i.e [1, 10, 13], num_to_letter (dictionary to convert values to cards,
    value_dict, wild_dict, colour_dict are sorted hands and colour=True 
    turns on its condition. Will return the two accum if able, otherwise
    returns None'''
    
    first_comb = []
    
    # Check if values can create two accum of 34
    if sum(value_hand) < 68:
        return None

    # All combinations that sum 34 and leave enough cards to create more
    for i in range(3, len(value_hand) - 2):
        for comb in combinations(value_hand, i):
            if sum(comb) == 34:
                first_comb.append(comb)
    
    # Find a second combination with remaining cards that sum to 34
    for comb_1 in first_comb:
        value_hand_copy = value_hand.copy()
        wild_list_copy = wild_list.copy()
        value_dict_copy = deepcopy(value_dict)
        
        # Creating leftover hand
        for card in comb_1:
            value_hand_copy.remove(card)
        
        # Create combinations summing to 34 with leftover hand
        for i in range(3, len(value_hand_copy) + 1):
            for comb_2 in combinations(value_hand_copy, i):
                value_hand_copy = value_hand.copy()
                
                # Reseting leftover hand
                for card in comb_1:
                    value_hand_copy.remove(card)
                    
                # Reseting hand for each combination
                wild_list_copy = wild_list.copy()
                value_dict_copy = deepcopy(value_dict)
                accum1, accum2 = [], []
                
                if sum(comb_2) == 34:
                    # If the both combinations sum to 34, replace cards
                    comb_1_cards = [i if i not in num_to_letter
                                    else num_to_letter[i] for i in comb_1]
                    for card in comb_1_cards:
                        if card != "A":
                            accum1.append(value_dict_copy[str(card)].pop())
                            
                        else:
                            accum1.append(wild_list_copy.pop())

                    comb_2_cards = [i if i not in num_to_letter
                                    else num_to_letter[i] for i in comb_2]
                    for card in comb_2_cards:
                        if card != "A":
                            accum2.append(value_dict_copy[str(card)].pop())
                            
                        else:
                            accum2.append(wild_list_copy.pop())

                    # If colour match, colour check both accum
                    if colour:
                        if colour_match(accum1, True):
                            if colour_match(accum2, True):
                                return [accum1, accum2]
                        
                        else:
                            # Try next combination
                            continue
                            
                    else:
                        return [accum1, accum2]
        
def run_check(wild_cards, wild_list, value_hand, run_length, num_to_letter, 
              value_dict, colour_dict, tried_comb, colour=False):
    ''' Takes wild_cards, wild_list, value_hand, value_dict, and colour_dict to
    attempt to create a run with a length of run_length. tried_comb ensures
    already attempted combinations are skipped. Will return a run of with
    a length of run_length and None if not. '''
    
    length = 0
    run = []
    play = []
    
    # Attempts to create a run starting from (2, K)
    for j in range(2, 14):
        wild_list_copy = wild_list.copy()
        value_dict_copy = deepcopy(value_dict)
        value_list_copy = value_hand.copy()
        
        # Attempts run with rotating start
        for x in range(j, 15):
            
            # Exits if length and ace limit correct
            if len(run) == run_length:
                aces = [i for i in run if i == 1]
                if len(aces) > run_length - 2:
                    run = []
                    continue
                if run in tried_comb:
                    run = []
                    continue
                break
            
            # Allows a run to loop past K by reseting
            if x == 14:
                for i in range(2, 13):
                    if len(run) == run_length:
                        aces = [i for i in run if i == 1]
                        if len(aces) > run_length - 2:
                            run = []
                            continue
                        if run in tried_comb:
                            run = []
                            continue
                        break
                        
                    # Check if consecutive card in hand, otherwise use ace
                    if i in value_list_copy:
                        run.append(i)
                        value_list_copy.remove(i)
                        continue
                    else:
                        if 1 in value_list_copy:
                            run.append(1)
                            value_list_copy.remove(1)
                            continue
                            # If no aces, break
                        else:
                            run = []
                            
                            break
                            
            # Condition check after break from loop past K
            if len(run) == run_length:
                aces = [i for i in run if i == 1]
                if len(aces) > run_length - 2:
                    run = []
                    continue
                if run in tried_comb:
                    run = []
                    continue

                break
            if x in value_list_copy:
                run.append(x)
                value_list_copy.remove(x)
                length += 1

                continue
            else:
                if 1 in value_list_copy:
                    run.append(1)
                    value_list_copy.remove(1)
                    length += 1
                    continue

                else:
                    run = []
                    length = 0
                    break
                    
    # Convert values to cards
    run = [i if i not in num_to_letter else num_to_letter[i] for i in run]
    
    # If no run is found, exit here
    if len(run) < run_length:
        return None
    
    # Colour check each card, otherwise, create run with cards and return it
    if colour:
        for card in run:
            incorrect_colour = True
            value_dict_copy = deepcopy(value_dict)
            
            if card != "A":
                while incorrect_colour:
                    value = value_dict_copy[str(card)].pop()
                    
                    if value[1] in colour:
                        play.append(value)
                        incorrect_colour = False
                        
            else:
                play.append(wild_list_copy.pop())
    else:
        for card in run:
            if card != "A":
                play.append(value_dict_copy[str(card)].pop())
                
            else:
                play.append(wild_list_copy.pop())
                
    return [play]

def set_check(wild_cards, value_dict, wild_list, length, sets):
    ''' Use wild_cards, value_dict, wild_list to create sets of card. 
    Sets can be by suit or value. The number of sets and the length of each 
    set can be altered. pass suit_dict as value_dict to check by suit'''
    
    value_set = 0
    wild_cards_copy = wild_cards
    play = []

    # Uses similar logic to Q1, however, sorts value list to play highest set
    for items in sorted(list(value_dict.items()), reverse=True):
        if len(items[1]) >= length:
            play.append(items[1][:length])
            value_set += 1
            
        # Play set with wild cards 
        elif len(items[1]) + wild_cards_copy >= length:
            if 1 < len(items[1]) < length:   
                wild_cards_copy -= length - len(items[1])
                
                # Append wild cards to hand (doesnt have them originally)
                for i in range(length - len(items[1])):
                    items[1].append(wild_list.pop())
                    
                play.append(items[1][:length])
                value_set += 1
                
            else:
                continue
                
        # if the correct numbers of sets are created, exit
        if value_set == sets:
            return play
        
        else:
            continue
            
    # If the code exits loop without returning previously return None
    return None
    
def phase_to_play(player_phase, hand):
    ''' Plays takes the players current phase and hand to return a valid phase
    to play '''
    
    # Initalise all variables and lists
    play = []
    phase = player_phase + 1
    wild_cards = 0
    accum_dict = {"A": 1, "0": 10, "J": 11, "Q": 12, "K": 13}
    num_to_letter = {1: "A", 10: "0", 11: "J", 12: "Q", 13: "K"}
    value_hand = [int(i[0]) if i[0] not in accum_dict 
                  else accum_dict[i[0]] for i in hand]
    
    value_dict = defaultdict(list)
    suit_dict = defaultdict(list)
    colour_dict = defaultdict(list)
    wild_list = []
    tried_comb = []
    
    for card in hand:
        if card[0] != "A":
            value_dict[card[0]].append(card)
            suit_dict[card[1]].append(card)
            if card[1] == "H" or card[1] == "D":
                colour_dict["R"].append(card[0])
            else:
                colour_dict["B"].append(card[0])
        else:
            wild_list.append(card)
            wild_cards += 1
            

    # Depending on phase, check if a phase can be played
    if phase == 1:
        play = set_check(wild_cards, value_dict, wild_list, 3, 2)
        
    elif phase == 2:
        play = set_check(wild_cards, suit_dict, wild_list, 7, 1)
                    
    elif phase == 3:
        play = accum_check(value_hand, num_to_letter, value_dict, wild_list,
                           colour_dict)

    elif phase == 4:
        play = set_check(wild_cards, value_dict, wild_list, 4, 2)
                    
    elif phase == 5:
        play = run_check(wild_cards, wild_list, value_hand, 8, num_to_letter,
                         value_dict, colour_dict, tried_comb)

    elif phase == 6:
        play = accum_check(value_hand, num_to_letter, value_dict, wild_list, 
                           colour_dict, True)
    
    elif phase == 7:
            play_1 = []
            black_value_hand1 = [i for i in colour_dict["B"]]
            red_value_hand1 = [i for i in colour_dict["R"]]
            black_value_hand = [int(i[0]) if i[0] not in accum_dict 
                                else accum_dict[i[0]]
                                for i in black_value_hand1]
            
            red_value_hand = [int(i[0]) if i[0] not in accum_dict 
                              else accum_dict[i[0]]
                              for i in red_value_hand1]
            
            for i in wild_list:
                black_value_hand.append(1)
                red_value_hand.append(1)
                    
            # Attempts to create a run with only black
            while True:
                output = run_check(wild_cards, wild_list, black_value_hand, 4, 
                                   num_to_letter, value_dict, colour_dict, 
                                   tried_comb, ["C", "S"])
                
                if output == [] or output is None:
                    break
                    
                for x in output:
                    tried_comb.append([int(i[0]) if i[0] not in accum_dict 
                                       else accum_dict[i[0]] for i in x])
                    play_1.append(x)
                
            # Create run with only black
            while True:
                output = run_check(wild_cards, wild_list, red_value_hand, 4, 
                                   num_to_letter, value_dict, colour_dict, 
                                   tried_comb, ["D", "H"])
                
                if output == [] or output is None:
                    break
                    
                for x in output:
                    tried_comb.append([int(i[0]) if i[0] not in accum_dict 
                                       else accum_dict[i[0]] for i in x])
                    
                    play_1.append(x)
            
            # When all colour runs are found attempt to create a four value set
            if play_1:
                for pot_play in play_1:
                    wild_cards_copy = wild_cards
                    value_dict_copy = deepcopy(value_dict)
                    wild_list_copy = wild_list.copy()
                    
                    # Creates the colour run
                    for card in pot_play:
                        if card[0] != "A":
                            value_dict_copy[card[0]].remove(card)
                        else:
                            wild_list_copy.pop()
                            wild_cards_copy -= 1
                    
                    # Attempt to create set
                    play_2 = set_check(wild_cards_copy, value_dict_copy,
                                       wild_list_copy, 4, 1)
                    
                    if play_2:
                        return [pot_play, play_2[0]]
                    
                    else:
                        continue
                        
            else:
                return None                              
            
    return play
                

def phazed_play(player_id, table, turn_history, phase_status, hand, discard):
    ''' Takes all game environment data to generate a valid play. Will output
    a play type from 1 to 5 with the appropriate data along with it '''
    
    value_order = "AKQJ098765432"
    hand_value = sorted(hand, key=lambda card: tuple(value_order.index(x)
                                                     for x in card[0]))
    
    accum_dict = {"A": 1, "0": 10, "J": 11, "Q": 12, "K": 13}
    num_to_letter = {1: "A", 10: "0", 11: "J", 12: "Q", 13: "K"}
    player_phase = phase_status[player_id]
    wild_cards = 8
    pick_discard = False
    value_dict = defaultdict(list)
    suit_dict = defaultdict(list)
    colour_dict = defaultdict(list)
    wild_list = []
    has_played_phase = table[player_id][0]
    
    # Check if a phase is playable
    play = phase_to_play(player_phase, hand)
    
    # Initalise dictionaries and lists
    for card in hand:
        if card[0] != "A":
            value_dict[card[0]].append(card)
            suit_dict[card[1]].append(card)
            if card[1] == "H" or card[1] == "D":
                colour_dict["R"].append(card[0])
            else:
                colour_dict["B"].append(card[0])
        else:
            wild_list.append(card)
            wild_cards += 1
            
    # If no play is found, attempt to find one "if" discard was in hand
    if not play and discard:
        hand_discard = hand.copy()
        hand_discard.append(discard)
        play_discard = phase_to_play(player_phase, hand_discard)
        
        if play_discard:
            pick_discard = True 
    
    # Check if player has drawn
    if turn_history:
        if turn_history[-1][0] == player_id:
            curr_player_turn = True
        else:
            curr_player_turn = False
    else:
        curr_player_turn = False
        
    # If first move of turn, draw
    if not curr_player_turn:
        # If adding discard allowed for a play, draw it
        if pick_discard:
            return (2, discard)
        
        else:
            return (1, None)
        
    # If a phase has been played onto your table, play onto others
    if table[player_id][0]:
        new_table = []
        
        # Checks table in reverse order
        for i in [3, 2, 1, 0]:
            new_table.append(table[i])
            
        # Check if any card in your hand can create a valid phase when played
        player_index = 4
        for sets in new_table:
            if sets[0] in [1, 2, 4, 5, 7]:
                group_index = -1
                player_index -= 1
                
                # Check for valid phases with cards for each group on table
                for group in sets[1]:
                    group_index += 1
                    group_length = len(group)
                    
                    # For sets, take a slice to test validity
                    for card in hand_value:
                        if sets[0] == 1:
                            group_copy = group[:3]
                            
                        if sets[0] == 2:
                            group_copy = group[:7]
                            
                        if sets[0] == 4:
                            group_copy = group[:4]
                            
                        if sets[0] == 7:
                            group_copy = group[:4]
                            
                        sets_copy = sets[1].copy()
                        
                        # For runs, check if a run with last digits as well
                        if sets[0] == 5 or sets[0] == 7 and group_index == 0:  
                            sets_copy2 = sets_copy.copy()
                            group_copy = group[-8:]
                            group_copy.pop(0)
                            group_copy.append(card)
                            sets_copy2.append(group_copy)
                            sets_copy2.remove(group)
                            
                            # Check if edited group is valid
                            find_group = phazed_phase_type(sets_copy2)
                            
                            if new_table[player_index][0] in find_group:
                                return (4, (card, (player_index, group_index,
                                                   group_length)))
                            
                            
                            # Check if the run is valid from start
                            sets_copy = sets[1].copy()
                            group_copy = group[:8]
                            group_copy.pop(-1)
                            group_copy.insert(0, card)
                            sets_copy.append(group_copy)
                            sets_copy.remove(group)
                            find_group = phazed_phase_type(sets_copy)
                            
                            # If the valid set is the same as the table, return
                            if table[player_index][0] in find_group:
                                return (4, (card, (player_index, group_index, 
                                                   0)))
                            else:
                                break
                            
                        # Check if card being played on a set is valid
                        if card[0] != "A":
                            group_copy.pop(0)
                            group_copy.append(card)
                            sets_copy.append(group_copy)
                            sets_copy.remove(group)
                            
                            find_group = phazed_phase_type(sets_copy)
                            
                            if new_table[player_index][0] in find_group:
                                return (4, (card, (player_index, group_index,
                                                   group_length)))

                        # If it is an ace, play it
                        else:
                            return (4, (card, (player_index, group_index,
                                               group_length)))
            # For accumulations
            else:
                hand_copy = hand.copy()
                group_index = -1
                player_index -= 1
                
                for group in sets[1]:
                    group_index += 1
                    group_length = len(group)
                    goal = 0
                    accum_values = [34, 55, 68, 76, 91, 94, 96, 97, 98]
                    set_sum = count_cards(group)

                    # Attempt to find original value of accum (if played on)
                    for i in range(len(accum_values)):
                        if accum_values[i] <= set_sum < accum_values[i + 1]:
                            try:
                                goal = accum_values[i + 1]
                                
                            except:
                                break
                                
                            break
                            
                    # Colour check if phase 6
                    if sets[0] == 6:
                        for card in group:
                            if card[1] in ["D", "H"]:
                                red = True    
                                break
                                
                            else:
                                red = False
                                break
                        
                        # Use only the correct colour
                        if red:
                            hand_colour = [i for i in hand if i[1] 
                                           in ["D", "H"]]
                            hand_copy = hand_colour
                            
                        else:
                            hand_colour = [i for i in hand if i[1] 
                                           in ["C", "S"]]
                            hand_copy = hand_colour
                    
                    # Find combination such that their sum is valid
                    for i in range(1, len(hand_copy) + 1):
                        for comb in combinations(hand_copy, i):
                            # Account for playing multiple series of plays
                            if count_cards(comb) == goal - set_sum:
                                return (4, (comb[0], (player_index,
                                                      group_index,
                                                      group_length)))


            
        
    # Check if a phase can be played. 
    if play and table[player_id][0] is None and play != [[]]:
        return(3, (player_phase + 1, play))
    
    # Else no moves left, so discard
    else:
        least_value_group = sorted(list(value_dict.values()),
                                   key=lambda x: len(x))
        
        least_suit_group = sorted(list(suit_dict.values()),
                                  key=lambda x: len(x))
        
        most_value_group = sorted(list(value_dict.values()),
                                  key=lambda x: len(x), reverse=True)
        
        # For sets
        if player_phase in [0, 3]:
            # When phase played, discard highest value card
            if has_played_phase:
                return (5, hand_value[0])
            
            # Otherwise, discard unique value card
            if least_value_group:
                return (5, least_value_group[0][0])
            
            else: 
                return (5, hand[-1])
        
        # For 7 suit
        if player_phase == 1:
            if has_played_phase:
                return (5, hand_value[0])
            
            # Discard unique suit card
            elif least_suit_group:
                return (5, least_suit_group[0][0])
            
            else: 
                return (5, hand[-1])
            
        # check if you already have an accumulation 
        if player_phase in [2, 5]:
            if has_played_phase:
                return (5, hand_value[0])
            
            return (5, hand[0])
        
        # For run
        if player_phase == 4:
            if has_played_phase:
                return (5, hand_value[0])
            
            # Discard duplicate cards Make highest
            elif most_value_group:
                return (5, most_value_group[0][0])
            
            else:
                return (5, hand[0])
            
        # For colour accum
        if player_phase == 6:
            if has_played_phase:
                return (5, hand_value[0])
            
            return (5, hand[0])
        
        # For phase 7
        if player_phase == 7:
            if has_played_phase:
                return (5, hand_value[0])
            
            else:
                pot_run = []
                run_cards = []
                black_value_hand1 = [i for i in colour_dict["B"]]
                red_value_hand1 = [i for i in colour_dict["R"]]
                black_value_hand = [int(i[0]) if i[0] not in accum_dict 
                                    else accum_dict[i[0]]
                                    for i in black_value_hand1]
                
                red_value_hand = [int(i[0]) if i[0] not in accum_dict 
                                  else accum_dict[i[0]]
                                  for i in red_value_hand1]
                
                for i in wild_list:
                    black_value_hand.append(1)
                    red_value_hand.append(1)
                    
                # Find run of 4 colour with black and red cards
                pot_run.append(run_check(wild_cards, wild_list,
                                         red_value_hand, 4, num_to_letter, 
                                         value_dict, 
                                         colour_dict, [], ["H", "D"])[0])
                
                pot_run.append(run_check(wild_cards, wild_list,
                                         black_value_hand, 4, num_to_letter,
                                         value_dict,
                                         colour_dict, [], ["S", "C"])[0])
                # Append cards to list
                for pot in pot_run:
                    for card in pot:
                        run_cards.append(card)
                        
                # Check hand with list, discard cards that are not in it
                for group in least_value_group:
                    for card in group:
                        if card not in run_cards:
                            return (5, card)

                        
                return (5, hand[0])


            


        

        
    
        
    

