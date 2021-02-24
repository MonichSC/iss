import math
import random
from simple_pid import PID


class PidController:
    def __init__(self, pid_params, target_temp, max_heater_power):

        self.max_heater_power = max_heater_power

        self.pid = PID(pid_params["temperature"]["p"], pid_params["temperature"]["i"], pid_params["temperature"]["d"])
        self.pid.setpoint = target_temp
        self.pid.sample_time = 1
        self.pid.output_limits = (0, 1)



    def tick(self, sim_object):

        new_power_factor = self.pid(sim_object.temperature[-1])

        sim_object.heater_status.append(1)    # always on
        sim_object.heater_power.append(new_power_factor * self.max_heater_power)
