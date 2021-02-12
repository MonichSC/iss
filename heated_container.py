import math


class Heated_container:
    def __init__(self,
                    start_level,
                    min_level,
                    max_level,
                    area,
                    start_temp,
                    target_temp,
                    max_temp_error,
                    max_heater_power,
                    input_temp,
                    max_input,
                    max_output,
                    start_in_valve_status,
                    start_out_valve_status,
                    beta):

        # Simulation parameters

        self.min_level = min_level                  # minimalna wysokosc cieczy
        self.max_level = max_level                  # maksymalna wysokosc cieczy
        self.area = area                            # powierzchnia zbiornika
        self.target_temp = target_temp              # temp. docelowa
        self.max_temp_error = max_temp_error        # tolerancja
        self.max_heater_power = max_heater_power    # maks. moc grzałki
        self.max_input = max_input                  # maks. przepustowość zaworu wejściowego
        self.max_output = max_output                # maks. przepustowość zaworu wyjściowego
        self.input_temp = input_temp                # temp. cieczy wpływającej

        self.beta = beta                            # beta

        # Simulation data

        self.level = [start_level]                          # bieżący poziom cieczy
        self.temperature = [start_temp]                     # bieżąca temp.
        self.error = [target_temp - start_temp]             # bieżący odchył
        self.heater_power = [0]                             # bieżąca moc grzałki
        self.in_valve_status = [start_in_valve_status]      # bieżące otwarcie zaworu wejściowego (0..1)
        self.input = [start_in_valve_status * max_input]    # ilość cieczy wpływającej
        self.out_valve_status = [start_out_valve_status]    # bieżące otwarcie zaworu wyjściowego (0..1)
        self.output = [start_out_valve_status * max_output] # ilość cieczy wypływającej


    def tick(self):

        # dla uproszczenia na początek przyjmijmy, że 1 tick = 1 sek.

        # level control

        new_input = self.max_input * self.in_valve_status[-1]
        self.input.append(new_input)

        print("new_input: " + str(new_input))

        print("self.out_valve_status[-1]: " + str(self.out_valve_status[-1]))

        new_output = self.max_output * self.out_valve_status[-1]
        self.output.append(new_output)

        print("new_output: " + str(new_output))

        new_level = self.level[-1] + (new_input - new_output) / self.area

        if new_level < 0:
            new_level = 0
        elif new_level > self.max_level:
            new_level = self.max_level

        self.level.append(new_level)

        print("new_level: " + str(new_level))


        # Temperature control

#        before_input_v = self.level[-2] * self.area
#        input_v = new_input
#        new_v = before_input_v + input_v

#        if new_v != 0:
#            new_temp = (before_input_v*self.temperature[-1] + input_v*self.input_temp) / new_v
#            heaterQ = self.heater_power[-1] * self.max_heater_power
            # dT = Q / (ro * V * Cp * t)
#            new_temp += heaterQ / (997 * new_v * 4190)
#            self.temperature.append(new_temp)
#        else:
#            self.temperature.append(0)

#        self.error.append(self.target_temp - self.temperature[-1])


    def get_data(self):
        output = dict()
        output['level'] = self.level
        output['temperature'] = self.temperature
        output['error'] = self.error
        output['heater_power'] = self.heater_power
        output['input'] = self.input
        output['output'] = self.output
        return output
