import bot_players as bots
import poker_game as pg
import numpy as np
import fft_bot
import multiprocessing

def calculate_fft_fitness(tree, opponents = [bots.CallMachineBot, bots.HazardBot, bots.CheaterBot, bots.EVBot], hands = 1000):
    start_money = 20
    average = np.zeros(len(opponents))
    std_dev = np.zeros(len(opponents))
    for i, p2 in enumerate(opponents):
        game = pg.PokerGame(blind_increment = 2)
        players = [fft_bot.FFTBot(game, money=start_money, tree=tree), p2(game, money=start_money)]
        game.initialise_players(players, shuffle=False)
        game.run_hands(n=hands, player_money=start_money)
        history = game.history
        average[i] = np.average(history[players[0]]) - start_money
        std_dev[i] = np.std(history[players[0]])
    fitness = np.average(average)
    tree.fitness = fitness
    return fitness 



class FitnessCalculator:
    def __init__(self, 
                 tree, 
                 opponents = [bots.CallMachineBot, bots.HazardBot, bots.CheaterBot, bots.EVBot], 
                 hands = 1000, 
                 worker_count = 1):
        self.tree = tree
        self.opponents = opponents
        self.hands = hands
        self.worker_count = worker_count
        self.workers = []
        self.hands_per_worker = self.hands // self.worker_count
        self.queue = multiprocessing.Queue()
        
    def create_workers(self):
        processes = []
        queue = self.queue
        for _ in range(self.worker_count):
            process = multiprocessing.Process(target=calculate_fitness, args=(queue, self.tree, self.hands_per_worker, self.opponents))
            processes.append(process)
        self.processes = processes
        

    def run_workers(self):
        for process in self.processes:
            process.start()
        for process in self.processes:
            process.join()
        return self.result()
    
    def result(self):
        seznam = []
        while not self.queue.empty():
            seznam.append(self.queue.get())
        fitness = np.average(seznam)
        return fitness         

def calculate_fitness(queue, tree, hands_per_worker, opponents = [bots.CallMachineBot, bots.HazardBot, bots.CheaterBot, bots.EVBot]):
    start_money = 20
    average = np.zeros(len(opponents))
    std_dev = np.zeros(len(opponents))
    for i, p2 in enumerate(opponents):
        game = pg.PokerGame(blind_increment = 2)
        players = [fft_bot.FFTBot(game, money=start_money, tree=tree), p2(game, money=start_money)]
        game.initialise_players(players, shuffle=False)
        game.run_hands(n=hands_per_worker, player_money=start_money)
        history = game.history
        average[i] = np.average(history[players[0]]) - start_money
        std_dev[i] = np.std(history[players[0]])
    fitness = np.average(average)
    tree.fitness = fitness
    queue.put(fitness) 