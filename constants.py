from enum import Enum

# SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
# VALUES = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
# CARD_DISPLAY = 0

# SUITS = ['S', 'H', 'C', 'D']
SUITS = ['♠', '♥', '♧', '♢']
VALUES = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_DISPLAY = 1


# Possible thresholds for each tracked variable
POSSIBLE_THRESHOLDS = {
            "isPair" : [1, -1], 
            "isSameSuit": [1, -1],
            "highestCard" : list(range(-14, -2)) + list(range(2, 14)),
            "lowestCard" : list(range(-14, -2)) + list(range(2, 14)),
            "totalPot" : [-30, -20, -10, 10, 20, 30]
        }

GamePhase = Enum('GamePhase', ('ENDROUND', 'PREFLOP', 'FLOP', 'TURN', 'RIVER'))
Actions = Enum('Actions', ('FOLD', 'CALL', 'RAISE'))

