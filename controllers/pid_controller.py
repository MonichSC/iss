import math
import random
from simple_pid import PID


def return_correct_value(min_value, actual_value, max_value):
    return min(max(actual_value, min_value), max_value)


class PidController:
    def __init__(self, pid_params, target_temp, input_temp, max_heater_power):

        self.max_heater_power = max_heater_power

        self.pid = PID(pid_params["temperature"]["p"], pid_params["temperature"]["i"], pid_params["temperature"]["d"], setpoint = target_temp)
        self.pid.setpoint = target_temp
        self.pid.sample_time = 1
        self.pid.output_limits = (0, self.max_heater_power) 



    def tick(self, sim_object):

        new_power = self.pid(sim_object.temperature[-1])

        sim_object.heater_status.append(1)    # always on
        sim_object.heater_power.append(new_power)
