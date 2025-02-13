# Implementation of the class SimulateInterface for the EVCharger
import numpy as np

from Abstraction.SimulateInterface import SimulateInterface


class Simu2(SimulateInterface):

    def simula(self, config, **kwargs):
        """
            Simula el comportament de l'evcharger durant dia a nivell horari.
            Te en compte el consum global dels EVC en Amperes

            probabilities_of_car - un vector amb 24 integers amb el percentatge % (tant per 1) de la potencia que treballarem. 0 = minim, 100 = maxim charger.
            Tots els que controlem tenen la mateixa consigna.
                        exemple: [0,0,0,0,0,0,0,0,0.5,1,1,1,1,1,1,1,1,0.4,0,0,0,0,0,0]
        """

        simulation_kwargs = kwargs['kwargs_simulation']
        max_power = config['max_power']  # KWh
        calendar = config['calendar']
        potencies_keys = config['potencies_keys']
        simulation_hours = config['active_hours']
        active_calendar = config['active_calendar'].copy()

        potencies = []
        for hour in range(0, simulation_hours):
            key = str(int(calendar[hour]))
            potencies.append(potencies_keys[key])  # Calendari de potencies hora a hora

        min_amp_chargers = config['min_daily_charge']  # Amperatge minim
        max_amp_chargers = config['max_daily_charge']  # Amperatge maxim
        probabilities = config['probabilities_of_car']

        global_consumption = 0
        if simulation_kwargs.keys().__contains__('amp_consumption'):
            global_consumption = sum(simulation_kwargs['amp_consumption'])
        else:
            simulation_kwargs['amp_consumption'] = [0] * len(potencies)

        consumption_profile = []  # Kwh hora a hora
        amp_consumption = []  # Aamperes hora a hora
        return_dictionary = {}
        cost_total = 0
        total_consumed_kwh = 0
        total_consumed_amp = 0
        hores_simular = len(potencies)

        volts = 230

        for hora in range(0, hores_simular):  # per cada hora del dia

            power = max_power * (potencies[hora] / 100) * probabilities[hora]  # calculem el que gasta
            amp = power / volts * 1000
            total_consumed_amp += amp  # add the amperes consume

            if total_consumed_amp + global_consumption > max_amp_chargers:
                # if we exceed the daily limit, invalid solution

                cost_total = total_consumed_amp + global_consumption - max_amp_chargers
                break

            else:
                total_consumed_kwh += power
                consumption_profile.append(power)  # guardem el consum de l'hora actual a el perfil
                amp_consumption.append(amp)

        if not simulation_kwargs.keys().__contains__('n_charger'):
            simulation_kwargs['n_charger'] = 1
        else:
            simulation_kwargs['n_charger'] += 1

        if simulation_kwargs['n_charger'] == config['number_of_chargers'] and total_consumed_amp < min_amp_chargers:

            cost_total = min_amp_chargers - total_consumed_amp
            consumption_profile.pop()

            return_dictionary['consumption_profile'] = consumption_profile

        elif len(consumption_profile) < simulation_hours:
            return_dictionary['consumption_profile'] = consumption_profile

        else:

            if len(amp_consumption) == simulation_hours:
                simulation_kwargs['amp_consumption'] = np.add(amp_consumption, simulation_kwargs['amp_consumption'])

            consumption_profile_24h = [0.0] * 24  # format to 24h simulation
            for hora in range(len(consumption_profile)):
                index = active_calendar[0] + hora
                consumption_profile_24h[index] += consumption_profile[hora]

            return_dictionary['consumption_profile'] = consumption_profile_24h

        return_dictionary['cost_aproximacio'] = cost_total
        return_dictionary['consumed_Kwh'] = total_consumed_kwh

        return return_dictionary
        # retorna consum profile Kwh
