# Implementation of the class SimulateInterface for the HidrogenStation

# Aquesta simulació té en compte que es vol que els electrolyzers estiguin mínim 2 hores seguides produïnt
# Té en compte que hi poden haver molts tanks i molts electrolyzers. El qeu fa és calcular per cada hora quant
# generen tots els electrolyzers i ho reparteix per igual a tots els tanks.

from Abstraction.SimulateInterface import SimulateInterface
from Abstraction.Asset_types.Consumers.HidrogenStation.Electrolyzer import Electrolyzer
from Abstraction.Asset_types.Consumers.HidrogenStation.HidrogenTank import HidrogenTank


class Simu1(SimulateInterface):

    def simula(self, config, **kwargs):

        # Simula el comportament dels electrolitzadors i els tanks al llarg d'un dia a nivell horari.

        total_consumed_Kwh = 0  # kwh consumits en el dia
        electrolyzers_generated_kg = 0  # Kg generats en tot el dia (emmagatzemats + guardats)
        consumption_profile = []  # Kwh hora a hora
        total_under_cap = 0  # total under capacity sum of the tanks in kg
        tanks = kwargs['tanks']
        electrolyzers = kwargs['electrolyzers']
        max_power = config['max_power']

        active_hours = config['active_hours']
        active_calendar = config['active_calendar'].copy()

        n_consecutive = {}
        for elctro in electrolyzers:
            n_consecutive[elctro] = 0

        for hour in range(0, active_hours):  # per cada hora del dia

            electrolyzers_consumption, \
                electrolyzers_generated_kg, n_consecutive = self.__simulateElectrolyzers(self, electrolyzers, hour, active_hours, n_consecutive)

            if electrolyzers_consumption == -1 and electrolyzers_generated_kg == -1:
                return {'consumption_profile': consumption_profile}
                # consumption profile tindrà longitud < 24 ja que no s'ha complert la premisa
                # de produir un minim d'hores segides. AIXO S'HA DE TRACTAR QUAN ES CRIDA EL SIMULA DES DE FORA

            consumption_profile.append(0)
            consumption_profile[hour] += electrolyzers_consumption
            total_consumed_Kwh += electrolyzers_consumption

            under_cap, extra_kg = self.__simulateTanks(self, tanks, hour, electrolyzers_generated_kg)

            if under_cap != 0:
                total_under_cap += under_cap

            consumption_profile[hour] += max_power  # Base consumption per hour (standby)
            total_consumed_Kwh += max_power  # Base consumption per hour (standby)

        if total_under_cap != 0:
            consumption_profile.pop()  # solucio no valida

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        return_dictionary = {'consumption_profile': consumption_profile_24h,
                             'consumed_Kwh': total_consumed_Kwh,
                             'total_hidrogen_kg': extra_kg,
                             'cost_aproximacio': total_under_cap
                             }

        return return_dictionary
        # retorna consum profile Kw KWh consumits, total Kg generats, i quants kg sota capacitat minima estem

    def __calcProduction(self, electro: Electrolyzer, hour, active_hours):

        key = electro.config['calendar'][hour]
        consum = electro.partial_power[key]
        # afegim el que consumim en aquesta hora

        prod = electro.conversion_ratio[key]  # el que produirem

        # la primera hora despres d'engegar produeix nomes un 66%
        if electro.primer_cop:  # si és el primer cop avui i hem de generar
            electro.primer_cop = False  # suposem que el dia anterior estava ences...
        elif electro.consumed_profile[-1] == 0:
            prod = prod * 0.66

        electro.generated_kg += prod
        if len(electro.consumed_profile) < active_hours:
            electro.consumed_profile.append(consum)
        else:
            electro.consumed_profile[hour] = consum
            # guardem el que hem consumit aquesta hora

        return consum, prod

    def __checkMinimumConsecutiveHours(self, electro: Electrolyzer, hour, active_hours, n_consecutive):

        minimum_hours = electro.config['minimum_hour_production']
        minimum = True
        conscutive = n_consecutive

        if 0 < n_consecutive < minimum_hours:

            if electro.consumed_profile[hour] == 0:
                minimum = False

        elif n_consecutive >= minimum_hours and electro.consumed_profile[hour] == 0:
            conscutive *= 0

        elif n_consecutive == 0 and minimum_hours > 0 and electro.consumed_profile[hour] != 0:
            minimum = False or len(electro.consumed_profile) < active_hours - 1

        if minimum and electro.consumed_profile[hour] != 0:
            conscutive += 1

        return minimum, conscutive

    def __simulateElectrolyzers(self, electrolyzers, hour, active_hours, n_consecutive):

        total_consumed_kwh = 0
        total_generated_kg = 0
        consecutive = n_consecutive

        for key in electrolyzers:  # per cada electrolyzer

            electro: Electrolyzer = electrolyzers[key]

            consumption, generated_kg = self.__calcProduction(self, electro, hour, active_hours)
            total_consumed_kwh += consumption
            total_generated_kg += generated_kg

            minimum_consecutive_hours, consecutive[key] = self.__checkMinimumConsecutiveHours(self, electro, hour, active_hours, n_consecutive[key])

            if not minimum_consecutive_hours:
                return -1, -1, consecutive
                # retornem -1 si no hem estat el minim d'hores

        return total_consumed_kwh, total_generated_kg, consecutive

    def __simulateTanks(sel, tanks, hour, total_generated_kg):

        tank_under_capacity = {}  # hores durant les quals no s'ha complert el requisit de capacitat minima
        extra_kg = 0  # Kg generats de mes - vendre o llençar a l'atmosfera

        for tank in tanks.values():  # per cada tank

            tank: HidrogenTank
            tank_under_capacity[tank.name] = tank.tank_under_capacity  # equal to = 0

            tank_new_capacity = tank.actual_capacity + (total_generated_kg / len(tanks))
            # Repartim el que hem generat entre tots els tanks. Assumim que el que es genera es reparteix per
            # igual a tots els tanks

            if tank_new_capacity > tank.tank_max_capacity:  # si estem per sobre la capacitat del tanc cal alliberar

                extra_kg += tank_new_capacity - tank.tank_max_capacity  # afegim l'exedent que hem tingut
                tank_new_capacity = tank.tank_max_capacity  # posem el tanc al maxim de la seva capacitat

            elif tank_new_capacity < tank.tank_min_capacity:  # si estem per sota el minim marcat
                return tank.tank_min_capacity - tank_new_capacity, 0

            if len(tank.capacity_by_hours) < 24:
                tank.capacity_by_hours.append(tank_new_capacity)
            else:
                tank.capacity_by_hours[hour] = tank_new_capacity

            tank.actual_capacity = tank_new_capacity
            # ara la capacitat del tank es la correcte per tant la guardem

        return 0, extra_kg
