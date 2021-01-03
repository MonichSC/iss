import numpy as np
import matplotlib.pyplot as plt
import controllers.pid_controller as pctr
import controllers.null_controller as nctr
import heated_container as hc


class Simulation:
    def __init__(self, sim_object, controller):
        self.sim_object = sim_object
        self.controller = controller

    def run(self, simulation_time, ticks):
        for i in range(simulation_time * ticks):
            self.controller.tick(self.sim_object)
            self.sim_object.tick()


def launch_simulation(start_height=2, min_height=1, max_height=10, area=2,
                      start_temp=22, target_temp=66, max_temp_error=3, heater_max_power=2000,
                      max_fluid_input=0.1, input_fluid_temp=15, beta=0.035,
                      ticks_per_second=1000, sim_time=600, controller="none",
                      pid_parameters=None):
    if pid_parameters is None:
        pid_parameters = []
    sim_object = hc.Heated_container(start_height, min_height, max_height, area,
                                     start_temp, target_temp, max_temp_error, heater_max_power,
                                     max_fluid_input, input_fluid_temp, beta,
                                     ticks_per_second)

    if controller == "none":
        ctr = nctr.NullController()
    elif controller == "pid":
        if len(pid_parameters) == 0:
            pid_parameters = {
                "input": {
                    "p": 1, "i": 0.1, "d": 0.2
                },
                "output": {
                    "p": 1, "i": 0.1, "d": 0.2
                },
                "temperature": {
                    "p": 1, "i": 0.1, "d": 0.2
                }
            }
        ctr = pctr.PidController(pid_parameters, ticks_per_second)
    else:
        raise Exception("No such controller found")

    sim = Simulation(sim_object, ctr)
    sim.run(sim_time, ticks_per_second)
    return sim_object.get_data()


def make_plot(raw_data, name):
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


if __name__ == '__main__':
    print("START")
    raw_data = launch_simulation(controller="pid")

    make_plot(raw_data, "height")
    make_plot(raw_data, "temperature")
    make_plot(raw_data, "error")
    make_plot(raw_data, "input")
    make_plot(raw_data, "output")
    make_plot(raw_data, "heater_power")
    make_plot(raw_data, "input_valve")
    make_plot(raw_data, "output_valve")

    print("DONE")
