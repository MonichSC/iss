class NullController:

    def tick(self, sim_object):

        od = sim_object.get_data()   # object data

        sim_object.heater_status.append(od["heater_status"][-1])
        sim_object.heater_power.append(od["heater_power"][-1])
