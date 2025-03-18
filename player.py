from combinations import evaluate_hand

class Player:
    def __init__(self, game, name: str, money: int):
        self.game = game
        self.name = name
        self.hand = []
        self.hand_score = 0
        self.start_money = money
        self.money = money
        self.current_bet = 0
        self.total_bet = 0
        self.is_all_in = False
        self.bot = False


    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def print_hand(self):
        return print(f"\n{self.name} {self.hand} Money: {self.money}")

    def print_money(self):
        return print(f"{self.name} Money: {self.money}")
    
    def draw(self, deck, amount = 1):
        for _ in range(amount):    
            self.hand.append(deck.deal_card())
        return

    def reset_bet(self):
        self.current_bet = 0
        self.has_bet = False
        if self.money == 0:
            self.is_all_in = True
        else:
            self.is_all_in = False

    def reset_hand(self):
        self.hand = []
        self.hand_score = 0
        self.total_bet = 0
        self.is_all_in = False
    
    def choose_bet(self, biggest_bet):
        to_call = biggest_bet - self.current_bet
        print(f"To call: {to_call}")

        if self.money == 0:
            print("You are All-in.")
            self.has_bet = True
            return 0

        if to_call > self.money:
            while True:
                player_input = input(f"{self.name}, do you want to All-in (y) or fold (n)?")
                if player_input.lower().strip() in ["y", "yes", "all in", "all-in", "allin"]:
                    return self.move_money_to_pot(self.money) 
                elif player_input.lower().strip() in ["n", "no", "fold"]:
                    return -1

        while True:
            try:
                player_input = input(f"{self.name}, enter your bet: ")
                
                if player_input.lower().strip() == "call":
                    self.has_bet = True
                    return self.move_money_to_pot(to_call)
                if player_input.lower().strip() in ["all in", "all-in", "allin", "all"]:
                    self.has_bet = True
                    return self.move_money_to_pot(self.money) 
                if player_input.lower().strip() == "fold":
                    return -1
                
                bet_amount = int(player_input)
                if bet_amount > self.money:
                    print("You cannot bet more than the money you have.") 
                    continue
                if bet_amount < to_call:
                    print("You cannot bet less than the amount to call.")
                    continue
                
                self.has_bet = True
                return self.move_money_to_pot(bet_amount)
            
            except ValueError:
                print("Enter a number.")
    
    def call(self):
        bet = min(self.to_call, self.money)
        return self.move_money_to_pot(bet)
    
    def fold(self):
        return -1
    
    def raise_bet(self, biggest_bet, multiplier = 2):
        bet = min(multiplier*(biggest_bet - self.current_bet), self.money)
        return self.move_money_to_pot(bet)

    def move_money_to_pot(self, money):
        if self.money <= money:
            money = self.money
            self.is_all_in = True

        self.current_bet += money
        self.total_bet += money
        self.money -= money

        return money
    
    def gain_money(self, money):
        self.money += money

    def bet_blind(self, blind):
        bet_amount = min(blind, self.money)
        self.has_bet = True
        return self.move_money_to_pot(bet_amount)
    
    def get_hand_evaluated(self):
        self.best_hand, self.hand_score = evaluate_hand(self, self.game.community_cards)

    def reset_money(self):
        self.money = self.start_money