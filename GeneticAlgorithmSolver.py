from RouteManager import RouteManager
from Route import Route
import random
import numpy as np


class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.2, tournament_size=10, elitism=False):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def evolve(self, routes):
              
        new_population = RouteManager(routes.cities, self.population_size)

        elitismOffset = 0

        for pos_population in range(elitismOffset,new_population.population_size):
            parent1 = self.tournament(new_population)
            parent2 = self.tournament(new_population)
            child = self.crossover(parent1, parent2)
            new_population.set_route(pos_population,child)

        for pos_population in range(elitismOffset, new_population.population_size):
            self.mutate(new_population.get_route(pos_population))

        return new_population

    def crossover(self, parent1, parent2):
        child_rt = Route(self.cities)
        for x in range(0,len(child_rt.route)):
            child_rt.route[x] = None

        start_pos = random.randint(0,len(parent1.route))
        end_pos = random.randint(0,len(parent1.route))

        if start_pos < end_pos:
            for x in range(start_pos,end_pos):
                child_rt.route[x] = parent1.route[x]
        elif start_pos > end_pos:
            for i in range(end_pos,start_pos):
                child_rt.route[i] = parent1.route[i]

        for i in range(len(parent2.route)):
            if not parent2.route[i] in child_rt.route:
                for x in range(len(child_rt.route)):
                    if child_rt.route[x] == None:
                        child_rt.route[x] = parent2.route[i]
                        break   
        return child_rt

    def mutate(self, route_to_mut):
        if random.random() < self.mutation_rate:
            mut_pos1 = random.randint(0,len(route_to_mut.route)-1)
            mut_pos2 = random.randint(0,len(route_to_mut.route)-1)

            city1 = route_to_mut.route[mut_pos1]
            city2 = route_to_mut.route[mut_pos2]

            route_to_mut.route[mut_pos2] = city1
            route_to_mut.route[mut_pos1] = city2

        return None

    def tournament(self, curr_pop):    
        tournament = RouteManager(self.cities, self.tournament_size)
        for pos_population in range(0, self.tournament_size):      
            rand_id = int(random.random())
            tournament.set_route(pos_population, curr_pop.get_route(rand_id))
        fittest = tournament.find_best_route()
        return fittest    
    
