from fft import FFT
import bot_players as bots
from constants import GamePhase

class FFTBot(bots.BotPlayer):
    def __init__(self, game, name = "FFTBot", money = 50, tree = None, filepath = None, bot_dictionary = None):
        super().__init__(game, name, money)
        self.bot = True
        self.create_tree(tree, filepath, bot_dictionary)

    def print_nodes(self):
        self.tree.print_nodes()

    def create_tree(self, tree, filepath, bot_dictionary):
        if tree:
            self.tree = tree
            return
        
        tree = FFT()
        if bot_dictionary:
            tree.from_dict(bot_dictionary)
        elif filepath:
            tree.from_json(filepath)
        else:
            tree.create_tree()
        self.tree = tree

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True
        
        if self.game.game_phase != GamePhase.PREFLOP:   
            return self.limit_call()
        
        higher_card = max(self.hand[0].card_score, self.hand[1].card_score)
        lower_card = min(self.hand[0].card_score, self.hand[1].card_score)
        pot = self.game.pot 
        same_suit = self.hand[0].suit == self.hand[1].suit
        
        game_state = {
            "isPair" : (higher_card == lower_card), 
            "isSameSuit": same_suit,
            "highestCard" : higher_card,
            "lowestCard" : lower_card,
            "totalPot" : pot
        }
        
        action = self.tree.propagate(game_state) 

        if action == "raise":
            return self.limit_raise(biggest_bet)
        elif action == "call":
            return self.limit_call()
        elif action == "fold":
            return self.limit_fold()
        else:
            print(f"ERROR: Invalid action '{action}'")
            return self.limit_fold()
    
    def print_tree(self):
        self.tree.print_nodes()

    def to_json(self, filepath = None):
        return self.tree.to_json(filepath)
    
class PassiveFFT(FFTBot):
    def __init__(self, game, name = "PassiveFFTBot", money = 20):
        passive_bot_filepath = "./bots/passive_fft.json"
        super().__init__(game, name, money, filepath=passive_bot_filepath)
        
class AggressiveFFT(FFTBot):
    def __init__(self, game, name = "AggressiveFFTBot", money = 20):
        aggressive_bot_filepath = "./bots/aggressive_fft.json"
        super().__init__(game, name, money, filepath=aggressive_bot_filepath)

