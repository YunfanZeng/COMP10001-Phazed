# COMP10001-Phazed
## The Rules of Phazed
Phazed is a card game modified for play for the purposes of this assignment. The rules can be found in the source files.
## The Input
The program is able to play phazed by passing it the boardstate. The function will return a single action based on the information provided.

The function takes 5 arguments

`phazed_play(player_id, table, turn_history, phase_status, hand, discard)`

### player_id
An integer between 0 and 3 inclusive, indicating the ID of the player attempting the play. 
### table
A 4-element list of phase plays for each of Players 0—3, respectively. Each phase play is in the form of a 2-tuple indicating the phase type (as an integer or None, consistent with the output of phazed_phase_type) and a list of lists of cards (of the same format as for phazed_phase_type, but possibly with extra cards played to each of the groups in the phase). An empty phase for a given player will take the form (None, []). As an example of a full 4-player table, [(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S', '5D']]), (None, []), (None, [])] indicates that Players 0, 2 and 3 are yet to play a phase for the hand, and Player 1 has played Phase 1, in the form of a set of Twos and a set of Fives, the latter of which has had one extra card added to it. 
### turn_history
A list of all turns in the hand to date, in sequence of play. Each turn takes the form of a 2-tuple made up of the Player ID and the list if individual plays in the turn (based on the same format as for play above, with the one difference that for any draws from the deck, the card is indicated as 'XX' (as it is not visible to other players). For example, [(0, [(2, 'JS'), (5, 'JS')]), (1, [(2, 'JS'), (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))])] indicates that the hand to date is made up of two turns, on the part of Players 0 and 1, respectively. Player 0 first drew the Jack of Spades from the discard pile, then discarded the Jack of Spades (presumably they had a change of heart!). Player 1 then picked up the Jack of Spades from the discard pile, and played a phase, in the form of two sets of three cards of the same value (i.e. Phase 1). 
### phase_status
A 4-element indicating the phases that each of Players 0—3, respectively, have achieved in the . For example, [0, 4, 0, 0] indicates that Players 0, 2 and 3 have not got any phases, but Player 1 has achieved up to Phase 4. At the start of a game, this is initialised to [0, 0, 0, 0]. 
### hand
The list of cards that the current player holds in their hand, each of which is in the form of a 2-element string. 
### discard
The top card of the discard stack, in the form of a 2-element string (e.g. '3D'). 
    

An example input would be:

```
phazed_play(1, [(None, []), (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H', '0S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'), (5, 'JS')]), (1, [(2, 'JS'), (3, (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H']])), (4, ('0S', (1, 0, 8))), (4, ('JS', (1, 0, 9)))])], [0, 5, 0, 0], ['5D'], None)
```
> Source: The University of Melbourne

## The Output
The function outputs a 2-tuple. The first variable indicates the move type using an integer from 1-5. The second indicates the card and required information.

### 1
Pick up a card from the top of the deck at the start of the player's turn. In this case, the card at the top of the deck is unknown at the time the play is determined, so the play content is set to None (i.e. (1, None)). 
### 2
Pick up a card from the top of the discard pile at the start of the player's turn, with the play content taking the value of discard (e.g. (2, '2C')). 
### 3
Place a phase to the table from the player's hand, with the play type being the 2-tuple of the phase ID (see Q2) and phase (e.g. (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))). 
### 4
Place a single card from the player's hand to a phase on the table, with the play type being a 2-tuple made up of the card the player is attempting to play, and the position they are attempting to play it in, itself in the form of a 3-tuple indicating: (1) the player ID of the phase the card is to be placed on; (2) the group within the phase the card is to placed in; and (3) the index of the position within the group the card is to be played to. For example, (4, ('AD', (1, 0, 3))) indicates that an Ace of Diamonds is to be placed on the phase of Player 1, in Group 0 and index position 3 (i.e. it will be the fourth card in the first Group). 
### 5
Discard a single card from the player's hand, and in doing so, end the turn (e.g. (5, 'JS') indicates that a Jack of Spades is to be discarded). 

## The Outcome
Against the 432 undisqualified members in the tournament, the program achieved rank 45
![Tournament Final Ranking](https://github.com/YunfanZeng/COMP10001-Phazed/blob/main/Tournament/FinalRank.PNG?raw=true)
