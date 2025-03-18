from player import Player

class ConsolePlayer(Player):
    def __init__(self, name, money):
        super().__init__(name, money)
    
    def choose_bet(self, biggest_bet):
        to_call = biggest_bet - self.current_bet
        while True:
            player_input = input(f"{self.name}, enter your bet: ")
            if player_input.lower().strip() == "call":
                self.has_bet = True
                return self.move_money_to_pot(to_call)
            if player_input.lower().strip() in ["all in", "all-in", "allin", "all"]:
                self.has_bet = True
                return self.move_money_to_pot(self.money) 
            if player_input.lower().strip() == "fold":
                return -1