import math
import random
from simple_pid import PID


def return_correct_value(min_value, actual_value, max_value):
    return min(max(actual_value, min_value), max_value)


class PidController:
    def __init__(self, pid_parameters, target_temp, input_temp):

        self.temperature_pid = PID(pid_parameters["temperature"]["p"], pid_parameters["temperature"]["i"],
                                   pid_parameters["temperature"]["d"], setpoint = target_temp)
        self.temperature_pid.output_limits = (0, 1) 
        self.temperature_pid.SetPoint = target_temp
        self.tick_counter = 0

    def tick(self, sim_object):
        sim_object.in_valve_status.append(1)
        if self.tick_counter == 0:
            if random.random() <= 0.0005:
                self.tick_counter = 15
                sim_object.out_valve_status.append(random.random())
            else:
                sim_object.out_valve_status.append(0)
        else:
            self.tick_counter -= 1

        #print(sim_object.temperature[-1])

        sim_object.heater_power.append(self.temperature_pid(sim_object.temperature[-1], 1))
