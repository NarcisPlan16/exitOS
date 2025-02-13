# Simulation type number 1 of the Thermal Storage

from Abstraction.SimulateInterface import SimulateInterface
from Abstraction.Asset_types.Consumers.ThermalStorage import HeatPump
from Abstraction.Asset_types.Consumers.ThermalStorage import HeatTank


class Simu1(SimulateInterface):

    def simula(self, config, **kwargs):

        # Simula el thermalStorage al llarg de les hores, funcionament només amb electricitat

        max_power = config['max_power']
        active_hours = config['active_hours']

        tanks = kwargs['tanks']
        pumps = kwargs['pumps']
        season = kwargs['season']
        season_calendar = config['season_calendar']
        active_calendar = config['active_calendar'].copy()

        consumption_profile = []  # Kwh hora a hora
        total_consumed_Kwh = 0  # kwh consumits en el dia
        cost_aproximacio = 0

        self.__resetTanks(self, tanks)

        for hour in range(0, active_hours):

            consumption_profile.append(0)

            consumed_kwh, temp_exchange_kwt = self.__simulatePumps(self, pumps, hour, season_calendar[season])
            # simulem les pumps

            if consumed_kwh == -1:  # configuracio no valida
                return {'consumption_profile': consumption_profile}

            consumption_profile[hour] += consumed_kwh
            total_consumed_Kwh += consumed_kwh

            cost_aproximacio = self.__simulateTanks(self, tanks, temp_exchange_kwt) # repartim el que s'ha generat

            consumption_profile[hour] += max_power  # Base consumption per hour (standby)
            total_consumed_Kwh += max_power  # Base consumption per hour (standby)

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        return_dictionary = {
            'consumption_profile': consumption_profile_24h,
            'total_consumed_Kwh': total_consumed_Kwh,
            'cost_aproximacio': cost_aproximacio
        }

        return return_dictionary

    def __resetTanks(self, tanks):

        for tank in tanks.values():
            tank.actual_temperature = tank.initial_temperature # resetejem a temperatura inicial

    def __simulatePumps(self, pumps, hour, season):

        total_generated_heat_kwt = 0
        total_consumed_kwh = 0

        for pump in pumps.values():  # per cada pump

            pump: HeatPump

            consumption, generated_heat_kwt = self.calcProduction(self, pump, hour, season)  # obtenim producció
            total_consumed_kwh += consumption
            total_generated_heat_kwt += generated_heat_kwt

        return total_consumed_kwh, total_generated_heat_kwt

    def __simulateTanks(self, tanks, temp_exchange_kwt):

        aproximation_cost = 0

        for tank in tanks.values():  # per cada tank

            tank: HeatTank
            tank.actual_temperature += temp_exchange_kwt / len(tanks) # repartim per igual el que s'ha generat

            if temp_exchange_kwt > 0:  # és hivern ja que hem generat calor
                aproximation_cost += abs(tank.max_temperature - tank.actual_temperature)
            else:  # és estiu, hem generat fred
                aproximation_cost += abs(tank.actual_temperature - tank.min_temperature)

        return aproximation_cost

    def calcProduction(self, pump: HeatPump, hour, season):

        key = pump.config['calendar'][hour]
        consumption = pump.config['partial_power'][key] * pump.max_power
        production = consumption * pump.efficiency * season

        # obtenim el consum i a quin % de power encendrem la heat pump

        pump.generated_heat_celcius += production
        if len(pump.consumed_profile) < 24:
            pump.consumed_profile.append(consumption)
        else:
            pump.consumed_profile[hour] = consumption
            # guardem el que hem consumit aquesta hora

        return consumption, production
