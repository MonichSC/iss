import math
from simple_pid import PID


def return_correct_value(min_value, actual_value, max_value):
    return min(max(actual_value, min_value), max_value)


class PidController:
    def __init__(self, pid_parameters, ticks_per_second):
        self.input_pid = PID(pid_parameters["input"]["p"], pid_parameters["input"]["i"], pid_parameters["input"]["d"])
        self.input_pid.sample_time = 1 / ticks_per_second
        self.output_pid = PID(pid_parameters["output"]["p"], pid_parameters["output"]["i"],
                              pid_parameters["output"]["d"])
        self.output_pid.sample_time = 1 / ticks_per_second
        self.temperature_pid = PID(pid_parameters["temperature"]["p"], pid_parameters["temperature"]["i"],
                                   pid_parameters["temperature"]["d"])
        self.temperature_pid.sample_time = 1 / ticks_per_second

    def tick(self, sim_object):
        error = sim_object.error[-1]
        height_error = sim_object.height[-1] - (sim_object.max_height - sim_object.min_height) / 2

        sim_object.input_valve_status.append(return_correct_value(0, self.input_pid(height_error) / 10, 1))
        #sim_object.output_valve_status.append(return_correct_value(0, self.output_pid(error), 1))
        sim_object.output_valve_status.append(0)
        sim_object.heater_power.append(return_correct_value(0, self.temperature_pid(error) / 10, 1))
        #sim_object.heater_power.append(1)

        # self.sum += error
        # derivative = (error - self.last_error) / sim_object.ticks_per_second
        # control = sim_object.error[-1] * self.p + self.sum * self.i + self.d * derivative / sim_object.max_temp_error
        # sim_object.input_valve_status.append(1 - return_correct_value(0, control, 1))
        # sim_object.output_valve_status.append(1 - return_correct_value(0, control, 1))
        #
        # self.abs_sum += math.fabs(error)
        # derivative = (math.fabs(error) - math.fabs(self.last_error)) / sim_object.ticks_per_second
        # abs_control = math.fabs(sim_object.error[-1]) * self.p + self.abs_sum * self.i + self.d * derivative
        # abs_control *= sim_object.heater_max_power
        # abs_control /= sim_object.max_temp_error
        # sim_object.heater_power.append(return_correct_value(0, abs_control, sim_object.heater_max_power))

        self.last_error = error
