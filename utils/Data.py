

class Data:
    def __init__(self, city_positions):
        self.city_positions = city_positions
        self.nums_city = len(self.city_positions)

    def get_city_pos(self):
        return self.city_positions

    def get_city_num(self):
        return self.nums_city