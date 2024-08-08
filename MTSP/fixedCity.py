import numpy as np
from mealpy import PermutationVar, EOA, Problem
import random
from utils import plot
from utils import Data
from utils import models

# solving a problem: N travlers start at K fixed city, method similar to EVO_TSP2
# finish? yes

class MTSPFixedCity(Data):
    def __init__(self, city_positions, start_points, model):
        super().__init__(city_positions)
        self.start_points = start_points
        self.data = {
            "city_positions": Data.get_city_pos(self),
            "num_cities": Data.get_city_num(self),
            "num_travelers": len(start_points),
            "start_points": start_points,
        }
        self.bounds = PermutationVar(valid_set=list(range(0, self.data["num_cities"])), name="per_var")
        self.problem = MTspProblem(bounds=self.bounds, minmax="min", data=self.data)
        self.model = model

    def run(self):
        self.model.solve(self.problem)
        return self.model.g_best.target.fitness, \
               MTSPFixedCity.from_breakpoints_to_routes_with_startpoints(self.problem.get_breakpoints(), self.problem.decode_solution(self.model.g_best.solution)["per_var"], self.start_points)

    @staticmethod
    def from_breakpoints_to_routes_with_startpoints(breakpoints, routes, startpoints):
        route = [[startpoints[i]] for i in range(len(breakpoints))]
        output_route = []
        sum = 0
        for num in breakpoints:
            sum += num
            output_route.append(sum)
        output_route.insert(0, 0)
        for i in range(len(route)):
            routes.remove(route[i][0])
        for i in range(0, len(output_route) - 1):
            temp = routes[output_route[i]:output_route[i + 1]]
            for j in range(len(temp)):
                route[i].append(temp[j])
        return route

    @staticmethod
    def get_breakpoints(routes, num_travlers, startpoints):
        # 初始化子集列表
        subsets = [[startpoints[i]] for i in range(num_travlers)]
        for route in routes:
            r = random.randint(1, num_travlers)
            if route not in startpoints:
                subsets[r - 1].append(route)
        breakpoints = []
        for subset in subsets:
            breakpoints.append(len(subset)-1)
        return breakpoints

class MTspProblem(Problem):
    def __init__(self, bounds=None, minmax="min", data=None, **kwargs):
        self.data = data
        self.breakpoints = MTSPFixedCity.get_breakpoints(list(range(0, self.data["num_cities"])), self.data["num_travelers"], self.data["start_points"])
        super().__init__(bounds, minmax, **kwargs)

    @staticmethod
    def calculate_distance(city_a, city_b):
        # Calculate Euclidean distance between two cities
        return np.linalg.norm(city_a - city_b)

    @staticmethod
    def calculate_total_distance(routes, city_positions):
        # Calculate total distance of all routes in MTSP
        total_distance = 0
        for route in routes:
            num_cities = len(route)
            for idx in range(num_cities):
                current_city = route[idx]
                next_city = route[(idx + 1) % num_cities]  # Wrap around to the first city
                total_distance += MTspProblem.calculate_distance(city_positions[current_city],
                                                                                 city_positions[next_city])
        return total_distance

    def obj_func(self, x):
        x = self.decode_solution(x)
        self.breakpoints = MTSPFixedCity.get_breakpoints(x["per_var"], self.data["num_travelers"], self.data["start_points"])
        routes = MTSPFixedCity.from_breakpoints_to_routes_with_startpoints(self.breakpoints, x["per_var"], self.data["start_points"])
        fitness = self.calculate_total_distance(routes, self.data["city_positions"])
        return fitness

    def get_breakpoints(self):
        return self.breakpoints


models = models(epoch=1000, pop_size=30)
city_positions = np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
                           [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
                           [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
                           [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]])
start_points = [0, 5, 10]
for i in range(0, len(models.get_models())):
    p = MTSPFixedCity(city_positions, start_points, models.get_models()[i])
    score, res = p.run()
    print(res)
    plt = plot.PlotRoutes(city_positions, breakpoints=p.problem.get_breakpoints(), total_cost=score, algorithm_name=models.get_models()[i].name, sub_route_city=res)
    plt.run()

# # MTSP问题的数据
# mtsp_data = {
#     "city_positions": np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
#                                 [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
#                                 [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
#                                 [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]]),
#     "num_cities": 20,
#     "num_travelers": 3,
#     "start_points": [0, 5, 10],  # 三个旅行商的起点
# }
#
# bounds = PermutationVar(valid_set=list(range(0, mtsp_data["num_cities"])), name="per_var")
# # 使用带有约束条件的MTSP问题
# mtsp_problem_with_constraints = MTspProblemWithConstraints(bounds=bounds,
#                                                             minmax="min", data=mtsp_data)
#
# # 使用EOA算法解决MTSP问题
# model_mtsp = EOA.OriginalEOA(epoch=1000, pop_size=30)
# model_mtsp.solve(mtsp_problem_with_constraints)
#
# # 打印结果
# print(f"Best agent: {model_mtsp.g_best}")
# print(f"Best solution: {model_mtsp.g_best.solution}")
# print(f"Best fitness: {model_mtsp.g_best.target.fitness}")
# print(f"Best real scheduling: {mtsp_problem_with_constraints.decode_solution(model_mtsp.g_best.solution)}")
# print(f"Best breakpoints: {mtsp_problem_with_constraints.get_breakpoints()}")
#
# routes = utils.PlotRoutes.from_breakpoints_to_routes_with_startpoints(mtsp_problem_with_constraints.get_breakpoints(), mtsp_problem_with_constraints.decode_solution(model_mtsp.g_best.solution)["per_var"], mtsp_data["start_points"])
# print(f"Best real solution: {routes}")
# plot = utils.PlotRoutes(mtsp_data["city_positions"], mtsp_problem_with_constraints.get_breakpoints(), routes)
# plot.run()