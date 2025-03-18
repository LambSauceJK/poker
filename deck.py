import random

from card import Card
from constants import SUITS, VALUES

class Deck:
    def __init__(self, shuffled = True):
        self.cards = []
        self.create_deck()
        if shuffled:
            self.shuffle_deck()

    def create_deck(self):
        self.cards = []
        for suit in SUITS:
            for value in VALUES:
                self.cards.append(Card(suit, value))
    
    def reset_deck(self):
        self.cards = []
        self.create_deck()
        self.shuffle_deck()        
    
    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)
        
    def add_cards(self, cards):
        self.cards += cards

    def sample_cards(self, n):
        return random.sample(self.cards, n)
