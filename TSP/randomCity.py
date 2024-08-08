import numpy as np
from mealpy import PermutationVar, WOA, Problem, EOA
from utils import plot
from utils import Data
from utils import models
# random city

class TSPRandomCity(Data):
    def __init__(self, city_positions, model):
        super().__init__(city_positions)
        self.data = {
            "city_positions": Data.get_city_pos(self),
            "num_cities": Data.get_city_num(self),
        }
        self.bounds = PermutationVar(valid_set=list(range(0, self.data["num_cities"])), name="per_var")
        self.problem = TspProblem(bounds=self.bounds, minmax="min", data=self.data)
        self.model = model

    def run(self):
        self.model.solve(self.problem)
        return self.model.g_best.target.fitness, self.model.problem.decode_solution(self.model.g_best.solution)["per_var"]

class TspProblem(Problem):
    def __init__(self, bounds=None, minmax="min", data=None, **kwargs):
        self.data = data
        super().__init__(bounds, minmax, **kwargs)

    @staticmethod
    def calculate_distance(city_a, city_b):
        # Calculate Euclidean distance between two cities
        return np.linalg.norm(city_a - city_b)

    @staticmethod
    def calculate_total_distance(route, city_positions):
        # Calculate total distance of a route
        total_distance = 0
        num_cities = len(route)
        for idx in range(num_cities):
            current_city = route[idx]
            next_city = route[(idx + 1) % num_cities]  # Wrap around to the first city
            total_distance += TspProblem.calculate_distance(city_positions[current_city], city_positions[next_city])
        return total_distance

    def obj_func(self, x):
        x_decoded = self.decode_solution(x)
        route = x_decoded["per_var"]
        fitness = self.calculate_total_distance(route, self.data["city_positions"])
        return fitness
# example

models = models(epoch=1000, pop_size=30)
city_positions = np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
                           [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
                           [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
                           [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]])
for i in range(0, len(models.get_models())):
    p = TSPRandomCity(city_positions, models.get_models()[i])
    score, res = p.run()
    plt = plot.PlotRoutes(city_positions, total_cost=score, algorithm_name=models.get_models()[i].name, sub_route_city=res)
    plt.run()


# Define the positions of the cities
# city_positions = np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
#                            [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
#                            [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
#                            [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]])
# num_cities = len(city_positions)
# data = {
#     "city_positions": city_positions,
#     "num_cities": num_cities,
# }

# class TspProblem(Problem):
#     def __init__(self, bounds=None, minmax="min", data=None, **kwargs):
#         self.data = data
#         super().__init__(bounds, minmax, **kwargs)
#
#     @staticmethod
#     def calculate_distance(city_a, city_b):
#         # Calculate Euclidean distance between two cities
#         return np.linalg.norm(city_a - city_b)
#
#     @staticmethod
#     def calculate_total_distance(route, city_positions):
#         # Calculate total distance of a route
#         total_distance = 0
#         num_cities = len(route)
#         for idx in range(num_cities):
#             current_city = route[idx]
#             next_city = route[(idx + 1) % num_cities]  # Wrap around to the first city
#             total_distance += TspProblem.calculate_distance(city_positions[current_city], city_positions[next_city])
#         return total_distance
#
#     def obj_func(self, x):
#         x_decoded = self.decode_solution(x)
#         route = x_decoded["per_var"]
#         fitness = self.calculate_total_distance(route, self.data["city_positions"])
#         return fitness
#
#
# bounds = PermutationVar(valid_set=list(range(0, num_cities)), name="per_var")
# problem = TspProblem(bounds=bounds, minmax="min", data=data)
#
# model = WOA.OriginalWOA(epoch=100, pop_size=20)
# model.solve(problem)

# print(f"Best agent: {model.g_best}")                    # Encoded solution
# print(f"Best solution: {model.g_best.solution}")        # Encoded solution
# print(f"Best fitness: {model.g_best.target.fitness}")
# print(f"Best real scheduling: {model.problem.decode_solution(model.g_best.solution)}")      # Decoded (Real) solution