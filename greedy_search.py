import fft
import numpy as np
import fitness
import copy
import bot_players as bots

class GreedySearch():
    def __init__(self):
        self.best_tree = None
        self.best_fitness = -np.inf
        self.tree = None
        self.create_simple_fft()

    def run_greedy_search(self, hands = 100):
        self.hands = hands
        # self.iterate_leafs()
        self.iterate_statements()

    def create_simple_fft(self):
        tree = fft.FFT()
        bot_dictionary = {
            "fitness" : 0,
            "statements" : 2,
            "complexity" : 3,
            "conditions" : [{
                "isLeaf" : False,
                "isPair" : 0, 
                "isSameSuit": 0,
                "highestCard" : 0,
                "lowestCard" : 0,
                "cardDifference": 0,
                "totalPot" : 0,
                "action" : "raise"
            },
            {
                "isLeaf" : True,
                "action" : "call"
            }]}
        tree.from_dict(bot_dictionary)
        self.tree = tree
        self.node = tree.child
        
    def iterate_leafs(self):
        for leaf_action in ["fold", "call", "raise"]:
            self.tree.set_leaf_action(leaf_action)
            self.iterate_statements()
 
    def iterate_statements(self):
        possible_thresholds = self.tree.possible_thresholds
        
        # Single condition
        for variable, thresholds in possible_thresholds.items(): 
            for t in thresholds:
                self.node.set_condition(variable, t)
                self.find_fitness()
                print(variable, t)
                self.node.set_condition(variable, 0)
        
        # Double condition
        # for i, (variable1, thresholds1) in enumerate(possible_thresholds.items()): 
        #     for j, (variable2, thresholds2) in enumerate(possible_thresholds.items()): 
        #         if j <= i:
        #             continue
        #         for t1 in thresholds1:
        #             for t2 in thresholds2:
        #                 self.node.set_condition(variable1, t1)
        #                 self.node.set_condition(variable2, t2)
        #                 print(variable1, t1, variable2, t2)
        #                 self.find_fitness()
        #                 self.node.set_condition(variable1, 0)
        #                 self.node.set_condition(variable2, 0)

    def add_statement(self):
        pass

    def find_fitness(self):
        fit = fitness.calculate_fft_fitness(self.tree, hands=self.hands, opponents=[bots.EVBot])
        if fit > self.best_fitness:
            self.best_fitness = fit
            self.best_tree = copy.deepcopy(self.tree)
        return fit

    def save_best(self, filepath):
        self.best_tree.to_json(filepath)