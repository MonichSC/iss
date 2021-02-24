import random

class FuzzyController:
    def __init__(self, max_temp_error, max_heater_power):

        self.max_temp_error = max_temp_error
        self.max_heater_power = max_heater_power



    def tick(self, sim_object):

        reasons_raw = [
            # Reason 0 - temperature is below target
            (sim_object.target_temp - sim_object.temperature[-1]) / 100,
            # Reason 1 - temperature is above target
            (sim_object.temperature[-1] - sim_object.target_temp) / 100,
            # Reason 2 - water is not at max level
            sim_object.level[-1] / sim_object.max_level,
            # Reason 3 - water is below minimum
            (sim_object.min_level - sim_object.level[-1]) / sim_object.min_level,
            # Reason 4 - temperature is within max_temp_error C of target
            # self.max_temp_error - abs(sim_object.temperature[-1] - sim_object.target_temp)
        ]

        reasons = []
        for r in reasons_raw:
            reasons.append(max(min(r, 1), 0))

        change = 0

        # Rule 0 - IF temperature is below target (R0) => heater power goes up
        change += reasons[0]

        # Rule 1 - IF temperature is above target (R1) => heater power goes down
        change += -reasons[1]*15

        new_power_factor = min(max(sim_object.heater_power[-1] + change / 100, 0), 1)

        sim_object.heater_status.append(1)    # always on
        sim_object.heater_power.append(new_power_factor * self.max_heater_power)
