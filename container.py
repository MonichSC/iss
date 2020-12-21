import math
class Container:
    # consts
    alpha = 1.5
    beta = 0.035
    Qd = 0.05
    Tp = 0.01
    maxH = 5

    def __init__(self, value):
        self.h = [value]

    def tick(self):
        qo = self.beta * math.sqrt(self.h[-1])
        new_h = (-qo + self.Qd) * self.Tp / self.alpha + self.h[-1]
        if new_h < 0:
            new_h = 0
        elif new_h > self.maxH:
            new_h = self.maxH
        self.h.append(new_h)

    def get_current_height(self):
        return self.h[-1]

    def get_heights(self):
        return self.h

    #def print(self):
    #   print(self.h)


def demo(start_h):
    obj = Container(start_h)
    for i in range(12 * 3600 * 100):
        obj.tick()
    return obj.get_heights()
