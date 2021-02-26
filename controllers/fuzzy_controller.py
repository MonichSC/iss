import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

ins = ['DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD']
outs = ['BDU', 'DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD', 'BDD']


class FuzzyController:
    def __init__(self, max_temp_error, target_temp, max_heater_power):

        self.max_temp_error = max_temp_error
        self.target_temp = target_temp
        self.max_heater_power = max_heater_power
        self.last_error = 0
        
        e = ctrl.Antecedent(np.arange(-50, 50, 0.1), 'e')
        ce = ctrl.Antecedent(np.arange(-0.5, 0.5, 0.001), 'ce')
        cu = ctrl.Consequent(np.arange(max_heater_power*-1, max_heater_power, 1), 'cu')

        e.automf(names=ins)

        ce.automf(names=ins)

        cu.automf(names=outs)


        # woda zbyt ciepła (uchyb ujemny)

        # BDU
        self.rules = [ctrl.Rule(e[ins[0]] & ce[ins[0]], cu[outs[0]])]
        self.rules.append(ctrl.Rule(e[ins[0]] & ce[ins[1]], cu[outs[0]]))
        self.rules.append(ctrl.Rule(e[ins[0]] & ce[ins[2]], cu[outs[0]]))
        self.rules.append(ctrl.Rule(e[ins[0]] & ce[ins[3]], cu[outs[0]]))
        self.rules.append(ctrl.Rule(e[ins[0]] & ce[ins[4]], cu[outs[0]]))
        self.rules.append(ctrl.Rule(e[ins[0]] & ce[ins[5]], cu[outs[0]]))
        self.rules.append(ctrl.Rule(e[ins[0]] & ce[ins[6]], cu[outs[0]]))
        # DU
        self.rules.append(ctrl.Rule(e[ins[1]] & ce[ins[0]], cu[outs[1]]))
        self.rules.append(ctrl.Rule(e[ins[1]] & ce[ins[1]], cu[outs[1]]))
        self.rules.append(ctrl.Rule(e[ins[1]] & ce[ins[2]], cu[outs[1]]))
        self.rules.append(ctrl.Rule(e[ins[1]] & ce[ins[3]], cu[outs[1]]))
        self.rules.append(ctrl.Rule(e[ins[1]] & ce[ins[4]], cu[outs[1]]))
        self.rules.append(ctrl.Rule(e[ins[1]] & ce[ins[5]], cu[outs[1]]))
        self.rules.append(ctrl.Rule(e[ins[1]] & ce[ins[6]], cu[outs[1]]))
        # SU
        self.rules.append(ctrl.Rule(e[ins[2]] & ce[ins[0]], cu[outs[2]]))
        self.rules.append(ctrl.Rule(e[ins[2]] & ce[ins[1]], cu[outs[2]]))
        self.rules.append(ctrl.Rule(e[ins[2]] & ce[ins[2]], cu[outs[2]]))
        self.rules.append(ctrl.Rule(e[ins[2]] & ce[ins[3]], cu[outs[2]]))
        self.rules.append(ctrl.Rule(e[ins[2]] & ce[ins[4]], cu[outs[2]]))
        self.rules.append(ctrl.Rule(e[ins[2]] & ce[ins[5]], cu[outs[2]]))
        self.rules.append(ctrl.Rule(e[ins[2]] & ce[ins[6]], cu[outs[2]]))
        # MU
        self.rules.append(ctrl.Rule(e[ins[3]] & ce[ins[0]], cu[outs[3]]))
        self.rules.append(ctrl.Rule(e[ins[3]] & ce[ins[1]], cu[outs[3]]))
        self.rules.append(ctrl.Rule(e[ins[3]] & ce[ins[2]], cu[outs[4]]))
        self.rules.append(ctrl.Rule(e[ins[3]] & ce[ins[3]], cu[outs[4]]))
        self.rules.append(ctrl.Rule(e[ins[3]] & ce[ins[4]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[3]] & ce[ins[5]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[3]] & ce[ins[6]], cu[outs[5]]))

        # w miarę OK

        # Z
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[0]], cu[outs[6]]))   # ujemne ce = błąd maleje = podtrzymujemy ciepło
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[1]], cu[outs[5]]))   # 5 lub 6?
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[2]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[3]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[4]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[5]], cu[outs[4]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[6]], cu[outs[3]]))   # dodatnie ce = szybko grzaliśmy = hamujemy

        # woda zbyt zimna (uchyb dodatni)
        # jeśli ce rośnie > 0 to za słabo grzejemy

        # MD
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[0]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[1]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[2]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[3]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[4]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[5]], cu[outs[5]]))
        self.rules.append(ctrl.Rule(e[ins[4]] & ce[ins[6]], cu[outs[5]]))
        # SD
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[0]], cu[outs[6]]))
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[1]], cu[outs[6]]))
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[2]], cu[outs[6]]))
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[3]], cu[outs[6]]))
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[4]], cu[outs[6]]))
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[5]], cu[outs[6]]))
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[6]], cu[outs[6]]))
        # DD
        self.rules.append(ctrl.Rule(e[ins[5]] & ce[ins[0]], cu[outs[7]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[1]], cu[outs[7]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[2]], cu[outs[7]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[3]], cu[outs[7]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[4]], cu[outs[7]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[5]], cu[outs[7]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[6]], cu[outs[7]]))
        # BDD
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[0]], cu[outs[8]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[1]], cu[outs[8]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[2]], cu[outs[8]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[3]], cu[outs[8]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[4]], cu[outs[8]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[5]], cu[outs[8]]))
        self.rules.append(ctrl.Rule(e[ins[6]] & ce[ins[6]], cu[outs[8]]))


        cu_ctrl = ctrl.ControlSystem(self.rules)
        self.reg_cu = ctrl.ControlSystemSimulation(cu_ctrl)



    def tick(self, sim_object):

        error = self.target_temp - sim_object.temperature[-1]
        error_change = error - self.last_error   # jeśli dodatni to się zwiększa
        self.last_error = error
        self.reg_cu.input['e'] = error
        self.reg_cu.input['ce'] = error_change
        self.reg_cu.compute()

        new_power = sim_object.heater_power[-1] + self.reg_cu.output['cu']

        if new_power > self.max_heater_power:
            new_power = self.max_heater_power
        elif new_power < 0:
            new_power = 0

        sim_object.heater_status.append(1)    # always on
        sim_object.heater_power.append(new_power)
