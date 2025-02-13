# Implementation of the class SimulateInterface for the Crane

import math

from Abstraction.SimulateInterface import SimulateInterface


class Simu1(SimulateInterface):

    def simula(self, config, **kwargs):
        """
            Simula el comportament dels cranes durant un dia a nivell horari.
            Ens arribaran el numero de moviments per cada hora.


            calendar - un vector indicant el nombre de moviments dins de cada hora
                       exemple: [1,3,4,5,1,6,2,3,4,3,4,2]
        """

        moviments = config['calendar']
        active_calendar = config['active_calendar'].copy()
        cost_per_movement = config['max_power']
        consumption_profile = []
        consumed_kwh = 0

        difference = int(config['minimum_movements_per_day'] - sum(moviments))
        # difference of movements between the total of the day and the minimum required

        if difference > 0:  # if minimum daily movmements condition is not met, no valid solution

            return {'consumption_profile': [0] * difference, 'consumed_kwh': difference}

        for hour in range(0, len(moviments)):  # per cada hora

            consum = moviments[hour] * cost_per_movement
            consumption_profile.append(consum)

            consumed_kwh += consum

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        return_dictionary = {'consumption_profile': consumption_profile_24h, 'consumed_kwh': consumed_kwh}

        return return_dictionary
        # retornem els kW gastats a cada hora i l'skedule de moviments
