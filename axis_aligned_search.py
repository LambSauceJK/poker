import fft
import json
import fitness
import copy 
import bot_players as bots
import numpy as np

class AxisAlignedSearch:
    def __init__(self):
        self.starting_tree = None
        self.current_tree = None
        self.forest = []
        self.best_tree = None
        self.best_fitness = -np.inf
        # clause pointer
        
    def run_axis_search(self, starting_tree = None, statements = 2, hands = 100, worker_count = 1):
        self.hands = hands
        self.worker_count = worker_count
        if starting_tree is not None:
            self.starting_tree = copy.deepcopy(starting_tree)
            self.current_tree = copy.deepcopy(starting_tree)
        else:
            self.create_tree(statements=statements)
        self.add_to_forest() # add starting tree to forest
        self.iterate_actions()
        self.iterate_clauses()

    def iterate_clauses(self):
        current_node = self.current_tree.child
        while current_node.leaf is False: 
            for condition, starting_threshold in current_node.conditions.items():
                if starting_threshold == 0 or condition == "action":
                    continue
                for threshold in current_node.possible_thresholds[condition]:
                    if threshold == starting_threshold:
                        continue
                    current_node.conditions[condition] = threshold
                    self.add_to_forest()
                current_node.conditions[condition] = starting_threshold 
            current_node = current_node.child

    def iterate_actions(self):
        current_node = self.current_tree.child
        while current_node is not None: 
            starting_action = current_node.action
            for action in ["call", "raise", "fold"]:
                if action == starting_action:
                    continue
                current_node.action = action
                self.add_to_forest()
            current_node.action = starting_action 
            current_node = current_node.child

    def create_tree(self, statements = None):
        # if statements = None, create a tree with a random number of statements (2-5)
        self.starting_tree = fft.FFT()
        self.starting_tree.create_tree(statements)
        self.starting_tree.randomize_statements()
        self.current_tree = copy.deepcopy(self.starting_tree)

    def add_to_forest(self):
        self.current_tree.count_statements()
        self.current_tree.count_complexity()
        self.find_fitness()
        self.forest.append(self.current_tree.to_json())   
    
    def find_fitness(self):
        # fit = fitness.calculate_fft_fitness(self.current_tree, hands=self.hands, opponents=[bots.EVBot])
        self.calculator = fitness.FitnessCalculator(self.current_tree, hands=self.hands, opponents=[bots.EVBot], worker_count=self.worker_count)
        self.calculator.create_workers()
        fit = self.calculator.run_workers()
        self.current_tree.fitness = fit
        if fit > self.best_fitness:
            self.best_fitness = fit
            self.best_tree = copy.deepcopy(self.current_tree)
        return fit
    
    def save_to_json(self, filepath):
        with open(filepath, 'w') as file:
            json.dump(self.forest, file, indent=4)

    