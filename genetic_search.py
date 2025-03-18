import random
import numpy as np
from fft import FFT
import fitness
import bot_players as bots
import time
import fft_bot
import json

class GeneticSearch:
    def __init__(self, population_size, generations, mutation_rate, hands = 100, worker_count = 1, opponents = [bots.EVBot], folder = "./bots/"):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.hands = hands
        self.worker_count = worker_count
        self.population = self.initialize_population()
        self.opponents = opponents
        self.folder = folder

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            tree = FFT()
            tree.create_tree()
            tree.randomize_statements()
            population.append(tree)
        return population

    def fitness(self, tree):
        if tree.fitness is not None:
            return tree.fitness
        calculator = fitness.FitnessCalculator(tree, hands=self.hands, opponents=self.opponents, worker_count=self.worker_count)
        calculator.create_workers()
        fit = calculator.run_workers()
        tree.fitness = fit
        return fit

    def selection(self):
        fitnesses = [self.fitness(tree) for tree in self.population]
        indices = np.argsort(fitnesses)[::-1]
        selected = [self.population[i] for i in indices[:self.population_size//2]]
        return selected

    def crossover(self, parent1, parent2):
        child_tree = FFT()
        child_tree.conditions = parent1.get_conditions()[:len(parent1.conditions)//2] + parent2.get_conditions()[len(parent2.conditions)//2:]
        child_tree.create_nodes()
        # print("\nParent 1")
        # parent1.print_nodes()
        # print("\nParent 2")
        # parent2.print_nodes()
        # print("\nChild")
        # child_tree.print_nodes()

        return child_tree

    def mutation(self, tree):
        # print("\nPre-Mutation")
        # tree.print_nodes()
        if random.random() < self.mutation_rate:
            tree.mutate_random_node()
        # print("\nMutant")
        # tree.print_nodes()
        tree.fitness = None
        return tree

    def save_generation(self):
        filepath = self.folder + "gen" + str(self.gen) + ".json"
        json_data = []
        for tree in self.population:
            json_data.append(tree.to_json())
        with open(filepath, "w") as file:
            json.dump(json_data, file)           

    def run(self):
        start_time = time.time()
        parent_size = int(((1-self.mutation_rate)*self.population_size)//2)
        for generation in range(self.generations):
            self.gen = generation
            selected = self.selection()
            self.save_generation()
            random.shuffle(selected)
            parents = selected[:parent_size].copy()
            mutation_victims = selected[parent_size:].copy()
            offspring = []
            while len(parents) > 1:
                parent1, parent2 = parents.pop(0), parents.pop(0)
                child = self.crossover(parent1, parent2)
                offspring.append(child)
                child = self.crossover(parent2, parent1)
                offspring.append(child)

            mutants = []
            for victim in mutation_victims:
                mutants.append(self.mutation(victim))
            
            self.population = selected + offspring + mutants
            best_tree = max(self.population, key=self.fitness)
            print(f"Generation {generation+1}, Best Fitness: {best_tree.fitness}, Pop size: {len(self.population)}, Execution time {time.time() - start_time:.2f} s")
            best_tree.print_nodes()
        return best_tree

if __name__ == "__main__":
    start_time = time.time()
    genetic_search = GeneticSearch(population_size=100, 
                                   generations=2, 
                                   mutation_rate=0.4, 
                                   hands = 100,
                                   worker_count=8,
                                   opponents=[bots.CheaterBot],
                                   folder="./bots/gs_cheater/")
    best_bot = genetic_search.run()
    end_time = time.time()
    print("Best Bot:")
    best_bot.print_nodes()
    print("Best fitness:", best_bot.fitness)
    print(f"Execution time {end_time - start_time:.2f} s")
