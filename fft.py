import json
import math
import random
from constants import POSSIBLE_THRESHOLDS

# Custom signum function
def sign(x):
    if x == 0:
        return 0
    return math.copysign(1, x)

class FFT:
    def __init__(self):
        self.child = None
        self.fitness = None
        self.statements = 0
        self.complexity = 0
        self.conditions = []
        self.possible_thresholds = POSSIBLE_THRESHOLDS

    def propagate(self, game_state):
        return self.child.propagate(game_state)

    def from_json(self, filepath):
        with open(filepath, "r") as file:
            bot_dictionary = json.load(file)
        self.from_dict(bot_dictionary)
    
    def from_dict(self, bot_dictionary):
        self.fitness = bot_dictionary["fitness"]
        self.statements = bot_dictionary["statements"]
        self.complexity = bot_dictionary["complexity"]
        self.conditions = bot_dictionary["conditions"]
        self.create_nodes()

    def create_nodes(self):
        current = self
        for condition in self.conditions:
            node = Node(condition)
            current.child = node
            current = current.child
        self.count_statements()
        self.count_complexity()

    def print_nodes(self):
        if self.child:
            self.child.print_nodes()

    def count_statements(self):
        current = self.child
        statements = 1
        while current.leaf is False:
            statements += 1
            current = current.child
        self.statements = statements
        return statements        
    
    def count_complexity(self):
        current = self.child
        complexity = 0
        while current is not None:
            for condition in current.conditions.values():
                if condition != 0:
                    complexity += 1
            complexity += 1
            current = current.child
        self.complexity = complexity
        return complexity 

    def create_tree(self, statements = None):
        if not statements:
            statements = random.randint(2, 5)
        self.conditions = []

        for _ in range(statements):
            self.conditions.append({
            "isLeaf" : False,
            "isPair" : 0, 
            "isSameSuit": 0,
            "highestCard" : 0,
            "lowestCard" : 0,
            "totalPot" : 0,
            "action" : "call"
        })
        self.conditions[-1]["isLeaf"] = True
        self.create_nodes()

    def randomize_statements(self):
        current = self.child       
        while not current.leaf:
            current.mutate_statement()
            current = current.child
        current.mutate_statement()
    
    def mutate_random_node(self):
        self.count_statements()
        node_index = random.randint(0, self.statements-1)
        current = self
        for i in range(self.statements):
            current = current.child
            if i == node_index:
                current.mutate_statement()
                break
        if self.all_same_action():
            current.set_different_action()
        self.count_complexity()        

    def get_conditions(self):
        conditions = []
        self.count_statements()
        current = self
        for i in range(self.statements):
            current = current.child
            node_info = current.conditions.copy()
            node_info["isLeaf"] = current.leaf
            node_info["action"] = current.action
            conditions.append(node_info)
        return conditions.copy()
    
    def to_json(self, filepath = None):
        conditions = self.get_conditions()
        data = {
            "fitness" : self.fitness,
            "statements" : self.statements,
            "complexity" : self.count_complexity(),
            "conditions" : conditions
            }
        
        if filepath is None:
            return data

        with open(filepath, 'w') as jsonfile:
            json.dump(data, jsonfile, indent = 4)

    def set_leaf_action(self, leaf_action):  
        current = self.child
        while not current.leaf:
            current = current.child
        current.action = leaf_action

    def all_same_action(self):
        current = self.child
        first_action = current.action
        current = current.child
        while current is not None:
            if current.action != first_action:
                return False
            current = current.child
        return True

class Node:
    def __init__(self, node_info = dict()):
        self.child = None
        self.action = node_info.pop("action")
        self.leaf = node_info.pop("isLeaf")
        self.conditions = node_info
        self.possible_thresholds = POSSIBLE_THRESHOLDS

    def condition(self, game_state):
        for key, value in game_state.items():
            if self.conditions[key] is None or self.conditions[key] == 0:
                continue

            if value is True:
                value = 0
            elif value is False:
                value = 1000
            
            threshold = self.conditions[key] 
            if sign(threshold) * value > threshold:
                return False
        return True
    
    def propagate(self, game_state):
        if self.leaf:
            return self.action
        if self.condition(game_state):
            return self.action
        return self.child.propagate(game_state)
    
    def print_nodes(self):
        if self.leaf:
            return print("else", self.action)
        print("if", end = " ")
        for key, value in self.conditions.items():
            value = int(value)
            if value == 0:
                continue
            sign = '<=' if value > 0 else '>='
            print(key, sign, abs(value), end = " ")
        print("then", self.action)
        if self.child:
            self.child.print_nodes()

    def mutate_statement(self):
        self.action = random.choice(["fold", "call", "raise"])
        if self.leaf:
            return        
        self.conditions = {
            "isPair" : 0, 
            "isSameSuit": 0,
            "highestCard" : 0,
            "lowestCard" : 0,
            "totalPot" : 0
        }

        # Set 1-2 random thresholds to random available values
        for condition in random.sample(list(self.conditions.keys()), random.randint(1,2)):
            self.conditions[condition] = random.choice(self.possible_thresholds[condition])

    def set_condition(self, variable, threshold):
        self.conditions[variable] = threshold
    
    def set_different_action(self):
        actions = ["fold", "call", "raise"]
        actions.remove(self.action)
        self.action = random.choice(actions)


if __name__ == "__main__":
    counter = 1
    for key in POSSIBLE_THRESHOLDS.keys():
        for value in POSSIBLE_THRESHOLDS[key]:
            counter += 1
    print(counter)