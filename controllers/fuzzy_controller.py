class FuzzyController:
    def __init__(self, max_temp_error):
        self.max_temp_error = max_temp_error

    def tick(self, sim_object):
        if len(sim_object.error) <= 2:
            sim_object.input_valve_status.append(sim_object.input_valve_status[-1])
            sim_object.output_valve_status.append(sim_object.input_valve_status[-1])
            sim_object.heater_power.append(sim_object.input_valve_status[-1])
            return

        reasons_raw = [
            # Reason 0 - temperature is below target
            (sim_object.target_temp - sim_object.temperature[-1]) / 100,
            # Reason 1 - temperature is above target
            (sim_object.temperature[-1] - sim_object.target_temp) / 100,
            # Reason 2 - water is not at max height
            sim_object.height[-1] / sim_object.max_height,
            # Reason 3 - water is below minimum
            (sim_object.min_height - sim_object.height[-1]) / sim_object.min_height,
            # Reason 4 - temperature is within max_temp_error C of target
            self.max_temp_error - abs(sim_object.temperature[-1] - sim_object.target_temp)
        ]

        reasons = []
        for r in reasons_raw:
            reasons.append(max(min(r, 1), 0))

        self.calculateInputControl(sim_object, reasons)
        self.calculateOutputControl(sim_object, reasons)
        self.calculateHeaterControl(sim_object, reasons)

    def calculateInputControl(self, sim_object, reasons):
        change = 0

        # Rule 0 - IF temperature is above target (R1) & water is not at max height (R2) => turn on input
        change += reasons[1] * reasons[2]
        # Rule 1 - IF temperature is below target (R0) => turn off input
        change += -reasons[0]
        # Rule 2 - IF water is below minimum (R3) => turn on input
        change += reasons[3]
        # Rule 3 - IF water is not at max height (R2) => turn off input
        change += -reasons[2]

        new_value = min(max(sim_object.input_valve_status[-1] + change / 100, 0), 1)
        sim_object.input_valve_status.append(new_value)

    def calculateOutputControl(self, sim_object, reasons):
        change = 0

        # Rule 0 - IF temperature is above target (R1) & water is not at min height (R3) => turn on output
        change += reasons[1] * reasons[2]
        # Rule 1 - IF height is below minimum (R3) => turn off output
        change += -reasons[3]
        # Rule 2 - IF temperature is below target (R0) => turn off output
        change += -reasons[0]
        # Rule 3 - IF temperature is close to target (R4) => turn on output
        change += reasons[4]

        new_value = min(max(sim_object.output_valve_status[-1] + change / 100, 0), 1)
        sim_object.output_valve_status.append(new_value)

    def calculateHeaterControl(self, sim_object, reasons):
        change = 0

        # Rule 0 - IF temperature is below target (R0) => heater power goes up
        change += reasons[0]
        # Rule 1 - IF temperature is above target (R1) => heater power goes down
        change += -reasons[1]

        new_value = min(max(sim_object.heater_power[-1] + change / 100, 0), 1)
        sim_object.heater_power.append(new_value)
