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
                      ticks_per_second=1000, sim_time=600, controller="none"):
    sim_object = hc.Heated_container(start_height, min_height, max_height, area,
                                     start_temp, target_temp, max_temp_error, heater_max_power,
                                     max_fluid_input, input_fluid_temp, beta,
                                     ticks_per_second)

    if controller == "none":
        ctr = nctr.NullController()
    else:
        raise Exception("No such controller found")

    sim = Simulation(sim_object, ctr)
    sim.run(sim_time, ticks_per_second)
    return sim_object.get_data()


if __name__ == '__main__':
    print("START")
    launch_simulation()
    print("DONE")
