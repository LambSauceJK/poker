from player import Player
from random import random, shuffle, randint, sample
from constants import GamePhase
from combinations import evaluate_hand

class BotPlayer(Player):
    def __init__(self, game, name = "BotPlayer", money = 50):
        super().__init__(game, name, money)
        self.bot = True

    def choose_bet(self, biggest_bet):
        return -1

    def print_hand(self):
        pass

    def limit_raise(self, biggest_bet):
        # Raise if possible
        if self.to_call != 0:       
            return self.raise_bet(biggest_bet)
        
        # Otherwise bet
        if self.game.game_phase == GamePhase.PREFLOP or self.game.game_phase == GamePhase.FLOP:
            return self.move_money_to_pot(2)
        return self.move_money_to_pot(4)
    
    def limit_call(self):
        return self.call()
    
    def limit_fold(self):
        if self.to_call == 0:
            return self.call()
        return self.fold()
    
class CheaterBot(BotPlayer):
    def __init__(self, game, name = "Podvodnik", money = 50, alcohol_resistance = 1):
        super().__init__(game, name, money)
        self.bot = True
        self.alcohol_resistance = alcohol_resistance

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True

        if self.game.game_phase != GamePhase.PREFLOP:   
            return self.limit_call()
        
        drink_strength = random()
        if drink_strength >= self.alcohol_resistance:
            decision = randint(0, 1)
            if decision == 0:
                return self.limit_raise(biggest_bet)
            elif decision == 1:
                return self.limit_fold()
            return self.limit_call()
 

        for player in self.game.players:
            if not isinstance(player, CheaterBot):
                self.opponent = player
                break
            
        # print(self.opponent.name)
        
        end_community = self.game.community_cards + self.game.deck.cards[:(5-len(self.game.community_cards))]
        _, opponent_score = evaluate_hand(self.opponent, end_community)
        _, my_score = evaluate_hand(self, end_community)
        
        # print(f"Cheater score = {my_score}, opponent score = {opponent_score}")
        
        if my_score >= opponent_score:
            return self.limit_raise(biggest_bet)
        return self.limit_fold()
    
class HazardBot(BotPlayer):
    def __init__(self, game, name = "Hazarder", money = 50):
        super().__init__(game, name, money)
        self.bot = True
    
    def choose_bet(self, biggest_bet):
        self.has_bet = True
        self.to_call = biggest_bet - self.current_bet
        
        if self.game.game_phase != GamePhase.PREFLOP:   
                return self.limit_call()
    
        return self.limit_raise(biggest_bet)

class CallMachineBot(BotPlayer):
    def __init__(self, game, name = "Dorovnavac", money = 50):
        super().__init__(game, name, money)
    
    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True
        bet = min(self.to_call, self.money)
        return self.move_money_to_pot(bet)


class IndifferentBot(BotPlayer):
    def __init__(self, game, name = "IndifferentBot", money = 50, thresholds = (0.3, 0.8, 0.99)):
        super().__init__(game, name, money)
        self.fold_threshold = thresholds[0]
        self.call_threshold = thresholds[1]
        self.raise_threshold = thresholds[2]

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True

        # check whenever it is possible
        if self.to_call == 0 or self.money == 0:
            bet = min(self.to_call, self.money)
            return self.move_money_to_pot(bet)

        r = random()
        if r < self.fold_threshold:
            return self.fold()
        elif r < self.call_threshold:
            return self.call()
        elif r < self.raise_threshold:
            # raise
            bet = min(2*biggest_bet - self.current_bet, self.money)
            return self.move_money_to_pot(bet)
        else:
            # all in
            return self.move_money_to_pot(self.money)
        

class NoobBot(BotPlayer):
    def __init__(self, game, name = "NoobBot", money = 50):
        super().__init__(game, name, money)
        self.bot = True

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True

        if self.game.game_phase == GamePhase.PREFLOP:   
            return self.call()
        self.get_hand_evaluated()  
        
        if self.to_call >= 5*self.game.big_blind: 
            return self.fold()
        
        if self.to_call == 0:
            if self.hand_score >= 10**9:
                bet = min(self.game.big_blind, self.money)
                return self.move_money_to_pot(bet)
            return 0 # Check
        
        if self.hand_score >= 10**9:
            return self.call()
        return self.fold()


class PreFlopBot(BotPlayer):
    def __init__(self, game, name = "PreflopBot", money = 50):
        super().__init__(game, name, money)
        self.bot = True

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True

        if self.game.game_phase == GamePhase.PREFLOP:   
            return self.preflop(biggest_bet)
        return self.postflop(biggest_bet)
    
    def preflop(self, biggest_bet):
        # preflop structure from paper
        higher_card = max(self.hand[0].card_score, self.hand[1].card_score)
        lower_card = min(self.hand[0].card_score, self.hand[1].card_score)
        pot_blinds = self.game.pot // self.game.big_blind
        has_pair = higher_card == lower_card
        # same_suit = self.hand[0].suit == self.hand[1].suit
        
        if lower_card <= 7 and higher_card <= 11:
            return self.call()
        elif pot_blinds <= 2:
            return self.raise_bet(biggest_bet, multiplier=2)
        elif has_pair:
            return self.raise_bet(biggest_bet, multiplier=3)
        elif pot_blinds >= 12:
            return self.fold()
        return self.call()
    
    def postflop(self, biggest_bet):
        self.get_hand_evaluated()  
        
        if self.to_call >= 5*self.game.big_blind: 
            return self.fold()
        
        if self.to_call == 0:
            if self.hand_score >= 10**9:
                bet = min(self.game.big_blind, self.money)
                return self.move_money_to_pot(bet)
            return 0 # Check
        
        if self.hand_score >= 10**9:
            return self.call()
        return self.fold()
    

class EVBot(BotPlayer):
    def __init__(self, game, name = "Evicka", money = 50, p_raise = 0.66, p_call = 0.33, n_sim = 10):
        super().__init__(game, name, money)
        self.bot = True
        self.p = -1
        self.p_raise = p_raise
        self.p_call = p_call
        self.n_sim = n_sim

    def reset_bet(self):
        self.current_bet = 0
        self.has_bet = False
        self.p = -1
        if self.money == 0:
            self.is_all_in = True
        else:
            self.is_all_in = False

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True

        if self.game.game_phase != GamePhase.PREFLOP:   
            return self.limit_call()
        
        if self.p == -1:
            self.p = self.simulate_hands()
        
        if self.p >= self.p_raise:
            return self.limit_raise(biggest_bet)
        elif self.p >= self.p_call:
            return self.limit_call()
        else:
            return self.limit_fold()
        
    def simulate_hands(self):
        for player in self.game.players:
            if player is not self:
                self.opponent = player
                break

        ghost_player = BotPlayer(self.game, "ghost", 1)
        wins = 0
        deck = self.game.deck.cards.copy() + self.opponent.hand.copy()
        for i in range(self.n_sim):
            shuffle(deck)
            opponent_hand = deck[:2]
            ghost_player.hand = opponent_hand
            community = self.game.community_cards.copy()
            community += deck[2:7-len(community)]
            _, opponent_score = evaluate_hand(ghost_player, community)
            _, my_score = evaluate_hand(self, community)
        
            if my_score > opponent_score:
                wins += 1

        return wins / self.n_sim

class CheaterHandsBot(BotPlayer):
    def __init__(self, game, name = "Evicka", money = 50, p_raise = 0.66, p_call = 0.33, n_sim = 10):
        super().__init__(game, name, money)
        self.bot = True
        self.p = -1
        self.p_raise = p_raise
        self.p_call = p_call
        self.n_sim = n_sim

    def reset_bet(self):
        self.current_bet = 0
        self.has_bet = False
        self.p = -1
        if self.money == 0:
            self.is_all_in = True
        else:
            self.is_all_in = False

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True

        if self.game.game_phase != GamePhase.PREFLOP:   
            return self.limit_call()
        
        if self.p == -1:
            self.p = self.simulate_hands()
        
        if self.p >= self.p_raise:
            return self.limit_raise(biggest_bet)
        elif self.p >= self.p_call:
            return self.limit_call()
        else:
            return self.limit_fold()
        
    def simulate_hands(self):
        for player in self.game.players:
            if player is not self:
                self.opponent = player
                break

        ghost_player = BotPlayer(self.game, "ghost", 1)
        wins = 0
        deck = self.game.deck.cards.copy()
        for i in range(self.n_sim):
            ghost_player.hand = self.opponent.hand.copy()
            community = self.game.community_cards.copy()
            community += sample(deck, 5-len(community))
            _, opponent_score = evaluate_hand(ghost_player, community)
            _, my_score = evaluate_hand(self, community)
        
            if my_score > opponent_score:
                wins += 1

        return wins / self.n_sim
  
class CheaterCommunityBot(BotPlayer):
    def __init__(self, game, name = "Evicka", money = 50, p_raise = 0.66, p_call = 0.33, n_sim = 10):
        super().__init__(game, name, money)
        self.bot = True
        self.p = -1
        self.p_raise = p_raise
        self.p_call = p_call
        self.n_sim = n_sim

    def reset_bet(self):
        self.current_bet = 0
        self.has_bet = False
        self.p = -1
        if self.money == 0:
            self.is_all_in = True
        else:
            self.is_all_in = False

    def choose_bet(self, biggest_bet):
        self.to_call = biggest_bet - self.current_bet
        self.has_bet = True

        if self.game.game_phase != GamePhase.PREFLOP:   
            return self.limit_call()
        
        if self.p == -1:
            self.p = self.simulate_hands()
        
        if self.p >= self.p_raise:
            return self.limit_raise(biggest_bet)
        elif self.p >= self.p_call:
            return self.limit_call()
        else:
            return self.limit_fold()
        
    def simulate_hands(self):
        for player in self.game.players:
            if player is not self:
                self.opponent = player
                break

        ghost_player = BotPlayer(self.game, "ghost", 1)
        wins = 0
        deck = self.game.deck.cards.copy() + self.opponent.hand.copy()
        for i in range(self.n_sim):
            community = self.game.community_cards.copy()
            community += deck[:5-len(community)]
            opponent_hand = sample(deck[5-len(community):], 2)
            ghost_player.hand = opponent_hand
            _, opponent_score = evaluate_hand(ghost_player, community)
            _, my_score = evaluate_hand(self, community)
        
            if my_score > opponent_score:
                wins += 1

        return wins / self.n_sim