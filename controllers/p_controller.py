class PController:
    def __init__(self, target_temp, input_temp, max_heater_power):
        self.target_temp = target_temp
        self.input_temp = input_temp
        self.max_heater_power = max_heater_power
        self.cnt = 0



    def tick(self, sim_object):

        od = sim_object.get_data()   # object data

        new_heater_status = od["heater_status"][-1]
        new_heater_power = od["heater_power"][-1]

        if od["temperature"][-1] < self.target_temp:
            if od["heater_status"][-1] == 0:
                print("heating...")
                new_heater_status = 1
                new_heater_power = self.max_heater_power
        elif od["temperature"][-1] >= self.target_temp:
            new_heater_status = 0
            new_heater_power = 0

        sim_object.heater_status.append(new_heater_status)
        sim_object.heater_power.append(new_heater_power)
        
        self.cnt += 1
        
        if self.cnt == 100:
            sim_object.out_valve_status.append(1)
        elif self.cnt == 200:
            sim_object.out_valve_status.append(0)
