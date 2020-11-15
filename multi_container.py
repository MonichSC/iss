import math

class multi_container:
    # Ticks per second
    Tp = 0.01
    # Maximum amount of water in a container
    max_height = 0
    # History of current amount of water in a container
    current_height = []
    # History of status of input value
    input_valve_status = []
    # History of status of output value
    output_valve_status = []
    # History of actual inputs and outputs
    input_history = []
    output_history = []
    # Area
    area = 1.5
    # Gravitational output const
    beta = 0.035

    def __init__(self, start_height, target_height, max_height, qi=0.1):
        self.max_height = max_height
        self.current_height.append(start_height)
        self.target_height = target_height
        # Start valves as closed
        self.input_valve_status.append(0)
        self.output_valve_status.append(0)
        # Simulation parameters
        self.max_input = qi

    def tick(self):
        # Control
        self.input_valve_status.append(1)
        self.output_valve_status.append(1)
        # Simulation
        input_per_second = self.max_input * self.input_valve_status[-1]
        output_per_second = self.output_valve_status[-1] * self.beta * math.sqrt(self.current_height[-1])

        self.input_history.append(input_per_second)
        self.output_history.append(output_per_second)

        new_height = self.current_height[-1] + (input_per_second - output_per_second) * self.Tp / self.area
        if new_height < 0:
            new_height = 0
        elif new_height > self.max_height:
            new_height = self.max_height
        self.current_height.append(new_height)

    def get_heights(self):
        return self.current_height


def demo(start_h):
    obj = multi_container(2, start_h, 10)
    for i in range(12 * 3600 * 100):
        obj.tick()
    return obj.get_heights()
