from ui import UI

class ConsoleInterface(UI):
    def __init__(self, game):
        super().__init__(game)
    
    def new_hand(self):
        print(f"HAND #{self.game.round}")
        print("Dealer:", self.game.dealer.name)

    def community_cards(self):
        print("Community", [str(x) for x in self.game.community_cards])
    
    def end_game(self):
        print(f"{self.game.players[0].name} WON THE GAME")

    def player_folded(self, player):
        print(f"Player {player.name} folded.")

    def player_bet(self, player, amount):
        print(f"{player.name} bet {amount} Current bet: {player.current_bet} Stack: {player.money} Pot: {self.game.pot}")

    def blinds_incremented(self):
        print(f"Blinds incremented to {self.game.small_blind}/{self.game.big_blind}.")
    
    def player_kicked(self, player):
        print(f"Player {player.name} lost.")

    def hand_results(self):
        print("---------------------------")

        # Community + best hands
        self.community_cards()
        for player in self.game.active_players:
            print(player.best_hand)

        print("---------------------------")

        # Winners
        if len(self.game.winners) == 1:
            print(f"{self.game.winners[0].name} WON the round!")
        elif len(self.game.winners) > 1:
            text = self.game.winners[0].name
            for w in self.game.winners[1:-1]:
                text += ", " + w.name
            text += f" and {self.game.winners[-1].name} are TIED and split the pot."
            print(text)
        else:
            print("ERROR: No winners")
        
        print("---------------------------")

        # Scoreboard   
        for player in self.game.players:
            player.print_money()

        print("---------------------------")

