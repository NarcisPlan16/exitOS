# Implementation of the class SimulateInterface for the EVCharger

from Abstraction.SimulateInterface import SimulateInterface


class Simu1(SimulateInterface):

    def simula(self, config, **kwargs):
        """
            Simula el comportament del cargador al llarg d'un dia a nivell horari.
        """

        consumed_Kwh = 0  # Kwh consumits en el dia
        consumption_profile = []  # Kwh hora a hora
        simulation_kwargs = kwargs['kwargs_simulation']
        hores_simulades = len(config['calendar'])
        max_power = config['max_power'] # Maxim per carregador
        calendar = config['calendar']
        active_calendar = config['active_calendar'].copy()  # we copy it because we are modifying its value

        for hour in range(0, hores_simulades):  # per cada hora del dia

            consumed_this_hour = max_power * calendar[hour]
            consumed_Kwh += consumed_this_hour  # afegim el que consumim en aquesta hora

            consumption_profile.append(consumed_this_hour)  # guardem el consum actual al perfil

        if not simulation_kwargs.keys().__contains__('n_charger'):
            simulation_kwargs['n_charger'] = 1
        else:
            simulation_kwargs['n_charger'] += 1

        if not simulation_kwargs.keys().__contains__('total_consumed_kwh'):
            simulation_kwargs['total_consumed_kwh'] = 0

        global_consumption = consumed_Kwh + simulation_kwargs['total_consumed_kwh']
        # global consumption of all evchargers
        minim = config['global_min_daily_charge']  # global minimum daily charge

        if simulation_kwargs['n_charger'] == config['number_of_chargers'] and global_consumption < minim:  # no arribem al minim diari

            longitud_bona = round((global_consumption / minim) * hores_simulades)
            # consumed_Kwh / maxim, ens dona el valor entre 0 i 1 que representa com de molt ens
            # hem apropat al minim diari de consum sent 1 el màxim aprop
            # longitud_bona serà 24 si s'ha consumit el minim diari, si no, < 24 i >= 0

            return_dictionary = {'consumption_profile': consumption_profile[0:longitud_bona],
                                 'consumed_Kwh': consumed_Kwh,
                                 'cost_aproximacio': minim - global_consumption
                                 }

            return return_dictionary

        cost = 0
        if global_consumption > minim:
            cost = global_consumption - minim

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        simulation_kwargs['total_consumed_kwh'] += consumed_Kwh

        return_dictionary = {'consumption_profile': consumption_profile_24h,
                             'consumed_Kwh': consumed_Kwh,
                             'cost_aproximacio': cost
                             }

        return return_dictionary
        # si no hem consumit el minim diari retornara un consumption profile amb len < 24
        # retorna consum profile Kw, KWh consumits
