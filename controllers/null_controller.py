class NullController:
    @staticmethod
    def tick(sim_object):
        barrel = sim_object.get_data()
#        if barrel["temperature"][-1] < 63:
#            print("heating...")
#            sim_object.heater_power.append(1)
#            sim_object.out_valve_status.append(0)
#        elif barrel["temperature"][-1] >= 66:
#            sim_object.heater_power.append(0)
#            sim_object.out_valve_status.append(1)
#        if  barrel["level"][-1] <= 1:
#            sim_object.in_valve_status.append(1)
#            sim_object.out_valve_status.append(0)
#        elif barrel["level"][-1] >= 5:
#            sim_object.in_valve_status.append(0)
        #sim_object.input_valve_status.append(1)
        #sim_object.output_valve_status.append(1)
        #sim_object.heater_power.append(0)

