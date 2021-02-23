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
                    heater_power,
                    input_temp,
                    max_input,
                    max_output,
#                    start_in_valve_status,
#                    start_out_valve_status,
#                    beta,
                    heater_status):

        # Simulation parameters

        self.min_level = min_level                  # minimalna wysokosc cieczy
        self.max_level = max_level                  # maksymalna wysokosc cieczy
        self.area = area                            # powierzchnia zbiornika
        self.target_temp = target_temp              # temp. docelowa
        self.max_temp_error = max_temp_error        # tolerancja
        self.heater_power = heater_power            # moc grzałki
        self.max_input = max_input                  # przepustowość zaworu wejściowego
        self.max_output = max_output                # przepustowość zaworu wyjściowego
        self.input_temp = input_temp                # temp. cieczy wpływającej
#        self.beta = beta                            # beta
        self.heater_status = heater_status          # grzałka włączona?

        # Simulation data

        self.level = [start_level]                          # bieżący poziom cieczy
        self.temperature = [start_temp]                     # bieżąca temp.
        self.error = [target_temp - start_temp]             # bieżący odchył
        self.input = [0]                                    # ilość cieczy wpływającej
        self.output = [0]                                   # ilość cieczy wypływającej
        self.in_valve_status = [1]                          # bieżące otwarcie zaworu wejściowego (0..1)
        self.out_valve_status = [0]                         # bieżące otwarcie zaworu wyjściowego (0..1)
        self.heater_status = [0]                            # bieżący status grzałki

        self.current=0
        self.max_current=30

#        print("self.out_valve_status[-1]: " + str(self.out_valve_status[-1]) + " (konstruktor)")


    def tick(self):

        # dla uproszczenia na początek przyjmijmy, że 1 tick = 1 sek.

        # level control

        new_input = self.max_input * self.in_valve_status[-1]
        self.input.append(new_input)

#        print("new_input: " + str(new_input))


#        print("self.out_valve_status[-1]: " + str(self.out_valve_status[-1]))

        new_output = self.max_output * self.out_valve_status[-1]
        self.output.append(new_output)

#        print("new_output: " + str(new_output))


        new_level = self.level[-1] + (new_input - new_output) / self.area

        if new_level <= self.min_level and self.out_valve_status[-1]==1:
            print("Awaryjne wylaczenie odplywu")
            self.out_valve_status.append(0)
#            new_level = self.min_level
        elif new_level >= self.max_level and self.in_valve_status[-1]==1:
            print("Wylaczenie doplywu")
            self.in_valve_status.append(0)
#            new_level = self.max_level

        self.level.append(new_level)

        if self.current == self.max_current:
            print("new_level: " + str(new_level))


        # Temperature control

        vol_before = self.level[-2] * self.area
        new_vol = new_level * self.area

        if self.current == self.max_current:
            print("new_vol: " + str(new_vol))

        # temp before heating

        new_temp = ((vol_before - new_output) * self.temperature[-1] + new_input * self.input_temp) / new_vol

        # temp with heating

        heaterQ = self.heater_status[-1] * self.heater_power

        # dT = Q / (mj * V * Cw * t)
        #
        # Q  - energia
        # mj - masa jednostkowa wody (ignorujemy zależność od temperatury)
        # V  - objętość
        # Cw - ciepło właściwe wody
        # t  - czas

        new_temp += heaterQ / (980 * new_vol * 4190)

        if self.current == self.max_current:
            print("new_temp: " + str(new_temp))


        # aktualizacja

        self.temperature.append(new_temp)

        self.error.append(self.target_temp - self.temperature[-1])


        # reset licznika printow

        if self.current == self.max_current:
            self.current = 0
        else:
            self.current += 1



    def get_data(self):
        output = dict()
        output['level'] = self.level
        output['temperature'] = self.temperature
        output['error'] = self.error
        output['heater_status'] = self.heater_status
        output['input'] = self.input
        output['output'] = self.output
        return output
