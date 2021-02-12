class NullController:
    @staticmethod
    def tick(sim_object):
        sim_object.in_valve_status.append(1)
        sim_object.out_valve_status.append(1)
        sim_object.heater_power.append(0)
