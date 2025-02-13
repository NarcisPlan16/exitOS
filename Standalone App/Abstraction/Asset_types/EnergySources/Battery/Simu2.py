# Implementation of the class SimulateInterface for the Battery

from Abstraction.SimulateInterface import SimulateInterface


class Simu2(SimulateInterface):

    def simula(self, config, **kwargs):
        """
            Simula el comportament de la bateria al llarg d'un dia a nivell horari.
        """

        max_capacity = config['max_capacity']  # Maximum in kwh
        cap_actual = config['cap_actual']  # Actual capacity in %
        efficiency = config['efficiency']  # Efficiency in range 0 - 1

        cap_actual_kwh = config['cap_actual'] * max_capacity  # Actual capacity in kwh
        bat_max = config['bat_max'] * max_capacity  # Maximum in kwh
        bat_min = config['bat_min'] * max_capacity  # Minimum in kwh

        percentage_keys = config['percentatges_keys']  # Potency percentages keys
        percentatges = config['calendar']
        active_calendar = config['active_calendar'].copy()

        consumption_profile = []

        # Ens passen el % que volem que tingui la nostra bateria.
        # ho convertim a % que hem de carregar o descarregar

        for hora in range(0, config['active_hours']):  # per cada hora del dia

            key = str(int(percentatges[hora]))
            percentage = percentage_keys[key]

            objective_kwh = max_capacity * percentage

            if percentage < cap_actual:  # Hem de descarregar
                consumption_profile.append(cap_actual_kwh - objective_kwh)

            elif percentage > cap_actual:  # Carreguem
                consumption_profile.append((objective_kwh - cap_actual_kwh) * (2 - efficiency))
                # (2 - efficiency) serà 1.01 si la eficiencia és 0.99,
                # per tant voldrà dir que hem de consumer un pèl més
            else:
                consumption_profile.append(0)

            cap_actual_kwh = percentage * max_capacity

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        return_dictionary = {'consumption_profile': consumption_profile_24h,
                             'actual_capacity_kwh': cap_actual_kwh
                             }

        return return_dictionary
        # si la solucio es valida o no, els kw que dona o xucla de xarxa la bateria
