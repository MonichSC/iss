class NullController:
    @staticmethod
    def tick(sim_object):
        sim_object.input_valve_status.append(1)
        sim_object.output_valve_status.append(1)
        sim_object.heater_power.append(0)
