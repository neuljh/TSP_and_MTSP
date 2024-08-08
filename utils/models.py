import numpy as np
from mealpy import EVO, GA, PSO, BBO, CHIO, CGO

class Models:
    def __init__(self, epoch, pop_size):
        self.epoch = epoch
        self.pop_size = pop_size
        self.models = []
        self.models.append(EVO.OriginalEVO(epoch=self.epoch, pop_size=self.pop_size))
        self.models.append(GA.BaseGA(epoch=self.epoch, pop_size=self.pop_size))
        self.models.append(PSO.OriginalPSO(epoch=self.epoch, pop_size=self.pop_size))
        self.models.append(BBO.OriginalBBO(epoch=self.epoch, pop_size=self.pop_size))
        self.models.append(CHIO.OriginalCHIO(epoch=self.epoch, pop_size=self.pop_size))
        self.models.append(CGO.OriginalCGO(epoch=self.epoch, pop_size=self.pop_size))

    def get_models(self):
        return self.models

