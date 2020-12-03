import math


class multi_container:

    def __init__(self, start_height, target_height, max_height, area=2.1, ticks_per_second=100, max_input=0.1,
                 beta=0.035):
        # Maximum amount of water in a container
        self.max_height = max_height
        # Target water amount
        self.target_height = target_height
        # Simulation parameters
        self.max_input = max_input
        self.beta = beta
        # Area of the container
        self.area = area
        # Ticks per second
        self.Tp = ticks_per_second
        # History of current amount of water in a container
        self.current_height = [start_height]
        # History of status of valves and water flow
        self.input_history = []
        self.output_history = []
        self.input_valve_status = []
        self.output_valve_status = []
        # Start valves as closed
        self.input_valve_status.append(0)
        self.output_valve_status.append(0)
        # Errors
        self.errors = []

    def tick(self):
        # Error calculation
        self.errors.append(self.target_height - self.current_height[-1])
        # Control values
        self.control()
        # Simulation
        input_per_second = self.max_input * self.input_valve_status[-1] / self.area
        output_per_second = self.output_valve_status[-1] * self.beta * math.sqrt(self.current_height[-1])

        self.input_history.append(input_per_second * self.area)
        self.output_history.append(output_per_second * self.area)

        new_height = self.current_height[-1] + (input_per_second - output_per_second) / self.Tp
        if new_height < 0:
            new_height = 0
        elif new_height > self.max_height:
            new_height = self.max_height
        self.current_height.append(new_height)

    def control(self):
        # For now input valve is always on
        self.input_valve_status.append(1)

        if len(self.errors) <= 2:
            self.output_valve_status.append(self.output_valve_status[-1])
            return

        # Reasons
        reasons_raw = [
            # Reason 0: error is falling
            abs(self.errors[-1]) - abs(self.errors[-2]),
            # Reason 1: error is raising
            abs(self.errors[-2]) - abs(self.errors[-1]),
            # Reason 2: error is positive
            self.errors[-1],
            # Reason 3: error is negative
            -self.errors[-1],
        ]

        reasons = []
        for r in reasons_raw:
            reasons.append(max(min(r, 1), 0))

        output_change = 0
        # Rule 1: IF error is positive (R2) => output_change is going up
        output_change += -reasons[2]
        # Rule 1: IF error is negative (R3) => output_change is going down
        output_change += reasons[3]

        new_output = min(max(self.output_valve_status[-1] + output_change, 0), 1)
        self.output_valve_status.append(new_output)

    def get_heights(self):
        return self.current_height


def demo(start_height, target_height=4, max_height=10, area=2, ticks_per_second=1000,
         max_input=0.1, beta=0.035, sim_time=600):
    """
    Launches simulation of the multi container
    Parameters
    ----------
    start_height : float
        Initial amount of water in the container specified in meters water column
    target_height : float
        Target for controller specified in meters water column
    max_height : float
        Maximum amount of water in the container specified in meters water column
    area : float
        Area of the base of the container specified in meters squared.
        This simulation assumes that cross section of the container is constant on any height of the container.
    ticks_per_second : int
        Number of simulation ticks performed every second.
    max_input : float
        Amount of water getting to the container through input pipe if value if open specified in m3/s.
    beta : float
        Parameter used to calculate the amount of water flowing out of the container on varying heights of water column.
    sim_time : int
        Simulation length in seconds.
    """
    obj = multi_container(start_height, target_height, max_height, area, ticks_per_second, max_input, beta)
    for i in range(sim_time * ticks_per_second):
        obj.tick()
    return obj.get_heights()


if __name__ == '__main__':
    print("START")
    demo(6)
    print("DONE")
