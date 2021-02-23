import numpy as np
import matplotlib.pyplot as plt
import controllers.null_controller as nctr
import controllers.p_controller as pctr
import controllers.pid_controller as pidctr
import controllers.fuzzy_controller as fctr
import heated_container as hc


class Simulation:
    def __init__(self, sim_object, controller):
        self.sim_object = sim_object
        self.controller = controller


    def run(self, sim_time):
        print(f"Running simulation for {sim_time} seconds")
        totalTicks = sim_time
        breakpointFactor = totalTicks / 20
        for i in range(totalTicks):
            if i % breakpointFactor == 0:
                print(f"{100*i/totalTicks}%")
            self.controller.tick(self.sim_object)
            self.sim_object.tick()


def launch_simulation(start_level,
                        min_level,
                        max_level,
                        area,
                        start_temp,
                        target_temp,
                        max_temp_error,
                        heater_power,
                        input_temp,
                        max_input,
                        max_output,
#                        start_in_valve_status=1,
#                        start_out_valve_status=0.1,
#                        beta,
                        sim_time,
                        controller,
                        pid_parameters):

    if pid_parameters is None:
        pid_parameters = []

    sim_object = hc.Heated_container(start_level,
                                        min_level,
                                        max_level,
                                        area,
                                        start_temp,
                                        target_temp,
                                        max_temp_error,
                                        heater_power,
                                        input_temp,
                                        max_input,
                                        max_output,
#                                        start_in_valve_status,
#                                        start_out_valve_status,
#                                        beta,
                                        0)      # heater_status

    if controller == "none":
        ctr = nctr.NullController()
    elif controller == "p":
        ctr = pctr.PController(target_temp, input_temp)
    elif controller == "pid":
        if len(pid_parameters) == 0:
            pid_parameters = {
#                "input": {
#                    "p": 5, "i": 1, "d": 0.01
#                },
#                "output": {
#                    "p": 0.3, "i": 0.5, "d": 0.0001
#                },
                "temperature": {
                    "p": 0.6, "i": 5, "d": -0.125
                }
            }
        else:
            print("recive_parameters")
        
        ctr = pidctr.PidController(pid_parameters, target_temp, input_temp)
    elif controller == "fuzzy":
        ctr = fctr.FuzzyController(max_temp_error)
    else:
        raise Exception("No such controller found")

    sim = Simulation(sim_object, ctr)
    sim.run(sim_time)
    return sim_object.get_data()


def make_plot(raw_data, name, id):
    data = raw_data[name]
    len_of_data = len(data)
    t = np.arange(0, len_of_data, 1)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(t, data, color='tab:blue')
    plt.xlabel('time')
    plt.ylabel('values')
    plt.xticks(np.arange(0, len_of_data + 1, len_of_data / 20))
    plt.grid(True)
    fig.set_size_inches(14, 4)
    fig.savefig('static/{0}.png'.format(name))
    print(f"{id}/8")


#if __name__ == '__main__':
#    print("START")
#    raw_data = launch_simulation(controller='fuzzy')
#    print("100.0%, generating diagrams")

#    make_plot(raw_data, "level", 1)
#    make_plot(raw_data, "temperature", 2)
#    make_plot(raw_data, "error", 3)
#    make_plot(raw_data, "input", 4)
#    make_plot(raw_data, "output", 5)
#    make_plot(raw_data, "heater_power", 6)
#    make_plot(raw_data, "input_valve", 7)
#    make_plot(raw_data, "output_valve", 8)

#    print("Finished")
