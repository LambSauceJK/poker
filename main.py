from poker_game import PokerGame
# import bot_players as bots
from player import Player
from fft_bot import FFTBot

# TODO List

# Nemusim delat: Cannot win more than what you bet -> Side pots
# Nemusim delat: Minimum raise

def main():
    game = PokerGame(console=True)
    players = [FFTBot(game, "FFTBot", 100, filepath="bots/first_fft.json"), Player(game, "Jarda", 100)]
    # players = [bots.CheaterBot(game, "Cheater", 100), Player(game, "Jarda", 100)]
    players[0].print_nodes()
    game.initialise_players(players)
    game.start_game()

if __name__ == "__main__":
    main()
