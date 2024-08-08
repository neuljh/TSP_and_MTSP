import numpy as np
import matplotlib.pyplot as plt
import math

from matplotlib.lines import Line2D


class PlotRoutes():
    def __init__(self, city_positions, total_cost, algorithm_name, breakpoints=None, sub_route_city=None):
        self.city_positions=city_positions
        self.pic_label1='City Positions'
        self.pic_label2=f"Cities with lines, Algorithm:{algorithm_name}, Total Cost ={str(round(total_cost, 3))}"
        self.breakpoints = breakpoints
        self.sub_route_city = sub_route_city
        if self.breakpoints is not None:
            self.colors = PlotRoutes.generate_random_colors(len(self.sub_route_city))
        else:
            self.colors = PlotRoutes.generate_random_colors(1)


    def is_valid_city_positions(self):
        if isinstance(self.city_positions, np.ndarray) and self.city_positions.shape[1] == 2:
            return True
        else:
            return False

    def plot_city_positions(self):
        plt.scatter(self.city_positions[:, 0], self.city_positions[:, 1], c='red', marker='o', label='City Positions')
        # 添加城市编号
        for i, pos in enumerate(self.city_positions):
            plt.text(pos[0], pos[1], str(i), fontsize=12, ha='right')
        plt.title(self.pic_label1)
        plt.xlabel('X')
        plt.ylabel('Y')

    # def add_line_city(self, x, y, color='blue'):
    #     # plt.plot(city_positions[x:y+1:y-x, 0], city_positions[x:y+1:y-x, 1], linestyle='-',
    #     #          color='blue', alpha=0.5)
    #     start = 0
    #     end = 0
    #     if x < y+1:
    #         start = x
    #         end = y+1
    #     else:
    #         start = y
    #         end = x+1
    #     plt.plot(self.city_positions[start:end:end-start-1, 0], self.city_positions[start:end:end-start-1, 1], linestyle='-', color=color, alpha=0.5)
    def add_line_city(self, x, y, color='blue', arrow_length=0.02):
        start = 0
        end = 0
        if x < y + 1:
            start = x
            end = y + 1
        else:
            start = y
            end = x + 1

        x_values = self.city_positions[start:end:end - start - 1, 0]
        y_values = self.city_positions[start:end:end - start - 1, 1]

        # Plot line
        plt.plot(x_values, y_values, linestyle='-', color=color, alpha=0.5)

        # # Add arrows
        # for i in range(len(x_values) - 1):
        #     dx = x_values[i + 1] - x_values[i]
        #     dy = y_values[i + 1] - y_values[i]
        #     plt.arrow(x_values[i], y_values[i], dx, dy, head_width=8, head_length=10, fc=color, ec=color)


    def plot_city_positions_with_lines(self):
        self.plot_city_positions()
        # 添加图例
        # Create custom legend
        legend_lines = [Line2D([0], [0], color=color, linestyle='-', alpha=0.5) for color in self.colors]
        legend_labels = [f'Route {i + 1}' for i in range(len(self.colors))]
        plt.legend(legend_lines, legend_labels)
        # 设置标题和坐标轴标签
        plt.title(self.pic_label2)
        plt.xlabel('X')
        plt.ylabel('Y')

    def run(self):
        if self.is_valid_city_positions():
            print("Input is valid.")
        else:
            print("Input is not valid.")
            return
        # self.plot_city_positions()
        # plt.show()
        if self.breakpoints is not None:
            for i in range(0, len(self.sub_route_city)):
                for j in range(0, len(self.sub_route_city[i])):
                    # 调用函数显示图形
                    if j == len(self.sub_route_city[i]) - 1:
                        self.add_line_city(self.sub_route_city[i][j], self.sub_route_city[i][0], self.colors[i])
                    else:
                        self.add_line_city(self.sub_route_city[i][j], self.sub_route_city[i][j + 1], self.colors[i])
        else:
            for i in range(0, len(self.sub_route_city)):
                if i == len(self.sub_route_city) - 1:
                    self.add_line_city(self.sub_route_city[i], self.sub_route_city[0],
                                       self.colors[0])
                else:
                    self.add_line_city(self.sub_route_city[i], self.sub_route_city[i + 1],
                                       self.colors[0])
        self.plot_city_positions_with_lines()
        plt.show()

    # @staticmethod
    # def generate_random_colors(size):
    #     # 随机生成RGB颜色值
    #     colors = np.random.rand(size, 3)
    #     # 将RGB值转换为合法的颜色字符串
    #     colors = [list(color) for color in colors]
    #     colors = ['#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255)) for [r, g, b] in colors]
    #     return colors

    @staticmethod
    def generate_random_colors(size):
        # 生成随机的HSV颜色
        hsv_colors = np.random.rand(size, 3)

        # 将HSV值转换为RGB
        rgb_colors = np.array([list(color) for color in PlotRoutes.hsv_to_rgb(hsv_colors)])

        # 将RGB值转换为合法的颜色字符串
        colors = ['#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255)) for [r, g, b] in rgb_colors]

        return colors

    @staticmethod
    def hsv_to_rgb(hsv_colors):
        # 将HSV颜色转换为RGB颜色
        rgb_colors = np.zeros_like(hsv_colors)
        for i in range(hsv_colors.shape[0]):
            rgb_colors[i] = PlotRoutes.hsv_to_rgb_single(hsv_colors[i])
        return rgb_colors

    @staticmethod
    def hsv_to_rgb_single(hsv_color):
        h, s, v = hsv_color
        if s == 0.0:
            return np.array([v, v, v])

        h = h * 6.0
        i = int(h)
        f = h - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))

        if i % 6 == 0:
            return np.array([v, t, p])
        elif i % 6 == 1:
            return np.array([q, v, p])
        elif i % 6 == 2:
            return np.array([p, v, t])
        elif i % 6 == 3:
            return np.array([p, q, v])
        elif i % 6 == 4:
            return np.array([t, p, v])
        else:
            return np.array([v, p, q])


# city_positions = np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
#                            [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
#                            [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
#                            [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]])
# test_plots = [7, 9, 15, 4, 17, 12, 3, 11, 14, 10, 8, 6, 0, 2, 1, 5, 16, 13, 18, 19]
# breakpoints = [5, 8, 7]
# test_plot = PlotRoutes.from_breakpoints_to_routes_without_startpoints(breakpoints, test_plots)
# plot = PlotRoutes(city_positions, breakpoints, test_plot)
# plot.run()

# plot = PlotRoutes(city_positions, sub_route_city=test_plots)
# plot.run()

# city_positions = np.array([[60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
#                            [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
#                            [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
#                            [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]])
#
# if is_valid_city_positions(city_positions):
#     print("Input is valid.")
# else:
#     print("Input is not valid.")
# plot_city_positions(city_positions)
# plt.show()
# # add_line_city(city_positions, 13, 16)
# # add_line_city(city_positions, 16, 13)
# # plot_city_positions_with_lines(city_positions)
# # plt.show()
# test_plots = [7, 9, 15, 4, 17, 12, 3, 11, 14, 10, 8, 6, 0, 2, 1, 5, 16, 13, 18, 19]
# breakpoints = [5, 8, 7]
# test_plot = [
#     [7, 9, 15, 4, 17],
#     [12, 3, 11, 14, 10, 8, 6, 0],
#     [2, 1, 5, 16, 13, 18, 19]
# ]
# colors = ['green', 'blue', 'yellow']
# for i in range(0, len(test_plot)):
#     # add_line_city(city_positions, test_plots[i], test_plots[i+1])
#     for j in range(0, len(test_plot[i])):
#         # 调用函数显示图形
#         if j == len(test_plot[i]) - 1:
#             # if test_plot[i][j] < test_plot[i][0]:
#             #     start = test_plot[i][j]
#             #     end = test_plot[i][0]
#             # else:
#             #     end = test_plot[i][j]
#             #     start = test_plot[i][0]
#             add_line_city(city_positions, test_plot[i][j], test_plot[i][0], colors[i])
#         else:
#             # if test_plot[i][j] < test_plot[i][j + 1]:
#             #     start = test_plot[i][j]
#             #     end = test_plot[i][j + 1]
#             # else:
#             #     end = test_plot[i][j]
#             #     start = test_plot[i][j + 1]
#             add_line_city(city_positions, test_plot[i][j], test_plot[i][j + 1], colors[i])
# # add_line_city(city_positions,0,8)
# plot_city_positions_with_lines(city_positions)
# plt.show()