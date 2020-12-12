import math


class Heated_container:
    def __init__(self, start_height, min_height, max_height, area,
                 start_temp, target_temp, max_temp_error, heater_max_power,
                 max_fluid_input, input_fluid_temp, beta,
                 ticks_per_second):
        # Simulation parameters
        self.min_height = min_height
        self.max_height = max_height
        self.area = area
        self.target_temp = target_temp
        self.max_temp_error = max_temp_error
        self.heater_max_power = heater_max_power
        self.max_fluid_input = max_fluid_input
        self.input_fluid_temp = input_fluid_temp
        self.beta = beta
        self.ticks_per_second = ticks_per_second
        # Simulation data
        self.height = [start_height]
        self.temperature = [start_temp]
        self.error = [target_temp - start_temp]
        self.input_history = [0]
        self.output_history = [0]
        self.heater_power = [0]
        self.input_valve_status = [0]
        self.output_valve_status = [0]

    def tick(self):
        # Height control
        input_per_second = self.max_fluid_input * self.input_valve_status[-1] / self.area
        output_per_second = self.output_valve_status[-1] * self.beta * math.sqrt(self.height[-1])
        self.input_history.append(input_per_second * self.area)
        self.output_history.append(output_per_second * self.area)
        new_height = self.height[-1] + (input_per_second - output_per_second) / self.ticks_per_second
        if new_height < 0:
            new_height = 0
        elif new_height > self.max_height:
            new_height = self.max_height
        self.height.append(new_height)
        # Temperature control
        fluid_before_input_v = self.height[-1] - output_per_second / self.ticks_per_second
        input_fluid_v = input_per_second / self.ticks_per_second
        new_fluid_v = fluid_before_input_v + input_fluid_v
        new_temp = (fluid_before_input_v*self.temperature[-1] + input_fluid_v*self.input_fluid_temp) / new_fluid_v
        self.temperature.append(new_temp)
        self.error.append(self.target_temp - new_temp)

    def get_data(self):
        output = dict()
        output['height'] = self.height
        output['temperature'] = self.temperature
        output['error'] = self.error
        output['input'] = self.input_history
        output['output'] = self.output_history
        output['input_valve'] = self.input_valve_status
        output['output_valve'] = self.output_valve_status
        return output
