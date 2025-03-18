from deck import Deck
from bot_players import BotPlayer
from combinations import evaluate_hand

class SimulationEnvironment:
    def __init__(self):
        self.players = []
        self.deck = Deck(shuffled=False)
        self.community_cards = []
        self.round = 0
        self.players = [BotPlayer(self, "Player 1", 100), BotPlayer(self, "Player 2", 100)]

    
    def simulate_hands(self, n=1000):
        wins = 0
        ties = 0

        for _ in range(n):
            community = self.deck.sample_cards(5)
            _, score0 = evaluate_hand(self.players[0], community)
            _, score1 = evaluate_hand(self.players[1], community)
            if score0 > score1:
                wins += 1
            elif score0 == score1:
                ties += 1

        return wins/n, ties/n
    
