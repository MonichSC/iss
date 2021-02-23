class PController:
    def __init__(self, target_temp, input_temp):
        self.target_temp = target_temp
        self.input_temp = input_temp

    def tick(self, sim_object):

        o = sim_object.get_data()

        new_heater_status = o["heater_status"][-1]

        if o["temperature"][-1] < self.target_temp:
            if o["heater_status"][-1] == 0:
                print("heating...")
                new_heater_status = 1
        elif o["temperature"][-1] >= self.target_temp:
            new_heater_status = 0

        sim_object.heater_status.append(new_heater_status)
