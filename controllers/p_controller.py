class PController:
    def __init__(self, target_temp, input_temp):
        self.target_temp = target_temp
        self.input_temp = input_temp

    def tick(self, sim_object):

        o = sim_object.get_data()

        if o["temperature"][-1] < self.target_temp:
            if o["heater_status"][-1] == 0:
                print("heating...")
                sim_object.heater_status.append(1)
        elif o["temperature"][-1] >= self.target_temp:
            sim_object.heater_status.append(0)

