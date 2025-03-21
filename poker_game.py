from math import floor
from deck import Deck
from console_interface import ConsoleInterface
import random
from ui import UI
from constants import GamePhase

class PokerGame:
    def __init__(self, small_blind=1, big_blind=None, console=False, blind_increment = 1):
        self.deck = Deck()

        self.small_blind = small_blind
        if big_blind is None:
            big_blind = 2*small_blind
        self.big_blind = big_blind

        if console:
            self.ui = ConsoleInterface(self)
        else:
            self.ui = UI(self)

        self.round = 0
        self.blind_period = 10 # number of rounds between blind increments
        self.blind_increment = blind_increment # increment of blinds 
        self.game_phase = GamePhase.ENDROUND

    def initialise_players(self, players, shuffle=True):
        self.players = players
        if shuffle:
            random.shuffle(self.players)
        self.history = dict((player, [player.money]) for player in self.players)

    def update_history(self):
        for player in self.players:
            self.history[player].append(player.money)

    def start_game(self):    
        while len(self.players) > 1:
            self.round += 1            
            self.increment_blinds()
            self.do_round()
            self.kick_players()
            self.update_history()
        self.ui.end_game()
        return 
    
    def run_hands(self, player_money, n):
        for i in range(n):
            self.do_round()
            self.update_history()
            for player in self.players:
                player.money = player_money
        return

    def do_round(self):
        self.deck.reset_deck()

        # Set the dealer and move him to last position  
        player = self.players.pop(0)
        self.players.append(player)
        self.dealer = player

        self.ui.new_hand()

        # Deal 2 cards to each player
        self.active_players = self.players.copy()
        for player in self.active_players:
            player.reset_hand()
            player.draw(self.deck, 2)
        
        self.community_cards = []
        self.pot = 0
        self.biggest_bet = 0
        self.pre_flop()
        if len(self.active_players) == 1:
            return self.end_round()
        self.flop()
        if len(self.active_players) == 1:
            return self.end_round()
        self.turn()
        if len(self.active_players) == 1:
            return self.end_round()
        self.river()
        self.end_round()
        
    
    def blinds(self):
        sb = self.players[0].bet_blind(self.small_blind) # Small blind
        bb = self.players[1].bet_blind(self.big_blind) # Big blind
        self.biggest_bet = max(sb, bb)
        self.pot += sb + bb

    def increment_blinds(self):
        if self.round % self.blind_period == 0:
            self.small_blind *= self.blind_increment
            self.big_blind *= self.blind_increment
            self.ui.blinds_incremented()
            
    def do_bets(self):
        # Player order
        self.active_players = [p for p in self.players if p in self.active_players]
        if self.game_phase == GamePhase.PREFLOP:
            self.active_players = self.active_players[2:] + self.active_players[:2]

        while True:
            # Check if all players have bet
            if [p for p in self.active_players if (p.current_bet == self.biggest_bet and p.has_bet) or p.is_all_in] == self.active_players:
                break
            player = self.active_players.pop(0)
            self.active_players.append(player)
            
            player.print_hand()
            if not player.bot:
                self.print_community()
            chosen_bet = player.choose_bet(self.biggest_bet)
            if chosen_bet >= 0:
                # Bet
                self.pot += chosen_bet
                self.biggest_bet = max([self.biggest_bet, player.current_bet])
                self.ui.player_bet(player, chosen_bet)
            elif chosen_bet == -1:
                # Fold
                self.ui.player_folded(player)
                self.active_players.remove(player)
                if len(self.active_players) == 1:
                    break
            else:
                print("Error: wrong bet")
            
    def pre_flop(self):
        self.game_phase = GamePhase.PREFLOP
        self.reset_bets()
        self.blinds()
        self.do_bets()
    
    def flop(self):
        self.game_phase = GamePhase.FLOP
        for _ in range(3):
            self.community_cards.append(self.deck.cards.pop(0))
        self.reset_bets()
        self.do_bets()

    def turn(self):
        self.game_phase = GamePhase.TURN
        self.community_cards.append(self.deck.cards.pop(0))
        self.reset_bets()
        self.do_bets()
        
    def river(self):
        self.game_phase = GamePhase.RIVER
        self.community_cards.append(self.deck.cards.pop(0))
        self.reset_bets()
        self.do_bets()

    def reset_bets(self):
        self.biggest_bet = 0
        for player in self.active_players:
            player.reset_bet()
        
    def end_round(self):
        self.game_phase = GamePhase.ENDROUND
        self.calculate_results()
        self.ui.hand_results()
    
    def print_community(self):
        self.ui.community_cards()

    def calculate_results(self):
        # Best hands of each player
        for player in self.active_players:
            player.get_hand_evaluated()
       
        # Winners
        winner = max(self.active_players, key=lambda p: p.hand_score)
        self.winners = [p for p in self.active_players if p.hand_score == winner.hand_score]
        
        self.share_pot(self.winners)

    def share_pot(self, winners):
        for player in winners:
            player.gain_money(floor(self.pot/len(winners)))
        self.pot = 0
    
    def kick_players(self):
        for player in self.players.copy():
            if player.money == 0:
                self.ui.player_kicked(player)
                self.players.remove(player)
