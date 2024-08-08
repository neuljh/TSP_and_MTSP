import numpy as np
from mealpy import PermutationVar, EOA, Problem
from utils import plot
from utils import Data
from utils import models
# # solving a problem: a travler start at a fixed city
# finish? yes
from utils.models import Models


class TSPFixedCity():
    def __init__(self, city_positions, start_city, model):
        super().__init__()
        self.city_positions = city_positions
        self.nums_city = len(self.city_positions)
        self.data = {
            "city_positions": self.city_positions,
            "num_cities": self.nums_city,
            "start_city":start_city
        }
        self.bounds = PermutationVar(valid_set=list(range(0, self.data["num_cities"])), name="per_var")
        self.problem = TspProblem(bounds=self.bounds, minmax="min", data=self.data)
        self.model = model

    def run(self):
        self.model.solve(self.problem)
        return self.model.g_best.target.fitness, \
               TSPFixedCity.get_fixed_startpoint_route(self.model.problem.decode_solution(self.model.g_best.solution)["per_var"], self.data["start_city"])


    @staticmethod
    def get_fixed_startpoint_route(routes, start_city):
        index = routes.index(start_city, 0, len(routes))
        routes = np.concatenate((routes[index:len(routes)], routes[0:index]), axis=0)
        routes = [int(route) for route in routes]
        return routes

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

    # Override the obj_func to consider the starting city
    def obj_func(self, x):
        # print(x)
        x_decoded = self.decode_solution(x)
        route = x_decoded["per_var"]
        route = TSPFixedCity.get_fixed_startpoint_route(route, self.data["start_city"])
        fitness = self.calculate_total_distance(route, self.data["city_positions"])
        return fitness

models = Models(epoch=1000, pop_size=30)
city_positions = np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
                           [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
                           [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
                           [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]])
start_city = 4
for i in range(0, len(models.get_models())):
    p = TSPFixedCity(
        city_positions=city_positions,
        start_city=start_city,
        model=models.get_models()[i]
    )
    score, res = p.run()
    plt = plot.PlotRoutes(city_positions, total_cost=score, algorithm_name=models.get_models()[i].name, sub_route_city=res)
    plt.run()

#
# # Define the positions of the cities
# city_positions = np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
#                            [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
#                            [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
#                            [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]])
# num_cities = len(city_positions)
# data = {
#     "city_positions": city_positions,
#     "num_cities": num_cities,
# }
#
# class TspProblem(Problem):
#     def __init__(self, bounds=None, minmax="min", data=None, **kwargs):
#         self.start_city = kwargs.get('start_city', 0)
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
#     # Override the obj_func to consider the starting city
#     def obj_func(self, x):
#         # print(x)
#         x_decoded = self.decode_solution(x)
#         route = x_decoded["per_var"]
#         route = get_fixed_startpoint_route(route, self.start_city)
#         print(route)
#         # # 添加约束条件
#         # # but this constraint condition sounds ridiculous
#         # if route[0] != self.start_city and self.start_city is not None:
#         #     return float('inf')  # 如果起始城市不是指定的城市，返回无穷大
#         fitness = self.calculate_total_distance(route, self.data["city_positions"])
#         return fitness
#
#
# # Specify the starting city (index of city A in city_positions)
# start_city_index = 4
# # Create an instance of PermutationVar with the starting city constraint
# valid_set = list(range(0, num_cities))
# print(f"valid_set{valid_set}")
# bounds_with_start = PermutationVar(valid_set=valid_set, name="per_var")
# # Create an instance of TspProblemWithStart
# problem_with_start = TspProblem(bounds=bounds_with_start, minmax="min", data=data, start_city=start_city_index)
#
#
# model = EOA.OriginalEOA(epoch=1000, pop_size=30)
# model.solve(problem_with_start)
#
# print(f"Best agent: {model.g_best}")                    # Encoded solution
# print(f"Best solution: {model.g_best.solution}")        # Encoded solution
# print(f"Best fitness: {model.g_best.target.fitness}")
# print(f"Best real scheduling: {model.problem.decode_solution(model.g_best.solution)}")      # Decoded (Real) solution