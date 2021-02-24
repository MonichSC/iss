class PController:
    def __init__(self, target_temp, max_heater_power):
        self.target_temp = target_temp
        self.max_heater_power = max_heater_power



    def tick(self, sim_object):

        od = sim_object.get_data()   # object data

        new_heater_status = od["heater_status"][-1]
        new_heater_power = od["heater_power"][-1]

        if od["temperature"][-1] < self.target_temp-1 and od["heater_status"][-1] == 0:
            print("heater on")
            new_heater_status = 1
            new_heater_power = self.max_heater_power
        elif od["temperature"][-1] >= self.target_temp+1 and od["heater_status"][-1] == 1:
            print("heater off")
            new_heater_status = 0
            new_heater_power = 0

        sim_object.heater_status.append(new_heater_status)
        sim_object.heater_power.append(new_heater_power)

