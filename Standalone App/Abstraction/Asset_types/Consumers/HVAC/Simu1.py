# Implementation of the class SimulateInterface for the HVac
import numpy as np

from Abstraction.SimulateInterface import SimulateInterface
import math


class Simu1(SimulateInterface):

    def simula(self, config, **kwargs):

        """
                Simula el comportament de l'HVAC al llarg d'un dia a nivell horari.

                temp_initial - temperatura inicial en K
                calendar - un vector amb 24 integers on 0 = apagat, 1 = ences
                            exemple: [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]

                            en cas de tenir restringides les hores d'operacio entrar nomes els valors necesaris
                            [1,1,1,1,1,1,1,0]
        """
        R = config['R']
        PC = config['PC']
        aux = math.exp(-1 / (R * config['C']))

        Tkk = config['temp_initial']
        temp_exterior = config['temp_exterior']
        temp_min = config['temp_min']
        temp_max = config['temp_max']

        calendar = config['calendar']
        active_calendar = config['active_calendar'].copy()

        temp = []
        maxim = 0
        minim = 0
        aproximacio = 0
        for i in range(len(calendar)):

            Tkk = aux * Tkk + R * (1 - aux) * PC * calendar[i] + (1 - aux) * temp_exterior[i]
            temp.append(Tkk)

            if Tkk < temp_min:

                maxim = temp_min - 0.01
                aproximacio += maxim - Tkk

            elif Tkk > temp_max:

                minim = temp_max + 0.01
                aproximacio += Tkk - minim

        consumption_profile = [i * abs(PC) for i in calendar]

        consumed_kwh = 0
        for consum in consumption_profile:
            consumed_kwh += consum

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        return_dictionary = {'consumption_profile': consumption_profile_24h,
                             'consumed_kwh': consumed_kwh,
                             'cost_aproximacio': abs(aproximacio)
                             }

        return return_dictionary
        # retorna la temperatura del perfil diari, kwh consumits i aproximacio
