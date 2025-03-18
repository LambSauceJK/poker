from constants import VALUES, CARD_DISPLAY

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.card_score = 14 - VALUES.index(value)
    
    def __str__(self):
        match CARD_DISPLAY:
            case 0:
                return f"{self.value} of {self.suit}"
            case 1:
                return f"{self.value}{self.suit}"
        
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (self.suit, self.value) == (other.suit, other.value)
    
    def __int__(self):
        return self.card_score