# Implementation of the class SimulateInterface for the HVac
import numpy as np

from Abstraction.SimulateInterface import SimulateInterface
from datetime import datetime

class Simu2(SimulateInterface):

    def simula(self, config, **kwargs):
        """
            Simula el comportament de l'HVAC al llarg d'un dia a nivell horari.
        """

        weekday = datetime.now().isoweekday()  # 1 is Monday and 7 is Sunday
        season = self.__getSeason(self)  # Obtenim l'estació en string
        exterior_temperatures = config['temp_exterior']
        mean_temp = sum(exterior_temperatures) / len(exterior_temperatures)  # temperatura mitjana

        active_hours = config['active_hours']
        active_calendar = config['active_calendar'].copy()

        consumption_profile = []  # consum en kwh al llarg del dia, hora a hora
        consumed_kwh = 0  # total consumit
        aproximacio = 0  # cost d'aproximacio al resultat desitjat

        if weekday < 6:
            operation, aproximacio = self.__calcConsumLaborable(self, season, mean_temp, active_hours, exterior_temperatures)
        else:
            operation, aproximacio = self.__calcConsumHoliday(self, season, mean_temp, active_hours, exterior_temperatures)

        consumption_profile = np.multiply(operation, config['max_power'])

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        return_dictionary = {'consumption_profile': consumption_profile_24h,
                             'consumed_kwh': consumed_kwh,
                             'cost_aproximacio': aproximacio
                             }

        return return_dictionary
        # retorna la temperatura del perfil diari, kwh consumits i aproximacio

    def __getSeason(self):

        # Obtenim el dia actual
        day = datetime.today().timetuple().tm_yday

        # Rang depen de l'hemisferi on estem
        spring = range(80, 172)
        summer = range(172, 264)
        autum = range(264, 355)
        # winter = la resta

        if day in spring:
            season = 'spring'
        elif day in summer:
            season = 'summer'
        elif day in autum:
            season = 'autum'
        else:
            season = 'winter'

        return season

    def __calcConsumLaborable(self, season, mean_temp, active_hours, temp_exterior):

        cost = 0
        operation = []

        electric = 20.2

        if season == "spring" or season == "autum":

            if mean_temp > 10:
                operation = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
                thermal = 260
            else:
                operation = [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
                thermal = 1200

            kWh = np.array(operation) * electric
            kWth = np.array(operation) * thermal

            for i in range(0, active_hours):
                if (temp_exterior[i] < 10 or temp_exterior[i] > 20) and operation[i] == 1:
                    kWh[i] = kWh[i] + 238
                    kWth[i] = kWth[i] + 744

        elif season == "summer":

            operation5 = [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            operation6 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

            kWh = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            kWth = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            operation = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

            for i in range(0, active_hours):
                if temp_exterior[i] < 20 and operation5[i] == 1:
                    kWh[i] = kWh[i] + 248
                    kWth[i] = kWth[i] + 657
                    operation[i] = 1
                if temp_exterior[i] > 35 and operation6[i] == 1:
                    kWh[i] = kWh[i] + 248
                    kWth[i] = kWth[i] + 657
                    operation[i] = 1

        else:  # winter

            thermal = 1200

            if mean_temp >= 10:
                operation = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            elif 0 < mean_temp < 10:
                operation = [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            else:
                operation = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
                thermal = 1460

            kWh = np.array(operation) * electric
            kWth = np.array(operation) * thermal

            for i in range(0, active_hours):
                if temp_exterior[i] < -10 and operation[i] == 1:
                    kWh[i] = kWh[i] + 2.2
                    kWth[i] = kWth[i] + 940

        return operation, cost

    def __calcConsumHoliday(self, season, mean_temp, active_hours, temp_exterior):

        cost = 0
        operation = []

        electric = 20.2

        if season == "spring" or season == "autum":

            if mean_temp > 10:
                operation = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                thermal = 260
            else:
                operation = [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                thermal = 1200

            kWh = np.array(operation) * electric
            kWth = np.array(operation) * thermal

            for i in range(0, active_hours):
                if (temp_exterior[i] < 10 or temp_exterior[i] > 20) and operation[i] == 1:
                    kWh[i] = kWh[i] + 238
                    kWth[i] = kWth[i] + 744

        elif season == "summer":

            operation5 = [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            operation6 = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            kWh = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            kWth = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            operation = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

            for i in range(0, active_hours):
                if temp_exterior[i] < 20 and operation5[i] == 1:
                    kWh[i] = kWh[i] + 248
                    kWth[i] = kWth[i] + 657
                    operation[i] = 1
                if temp_exterior[i] > 35 and operation6[i] == 1:
                    kWh[i] = kWh[i] + 248
                    kWth[i] = kWth[i] + 657
                    operation[i] = 1

        else:  # winter

            thermal = 1200

            if mean_temp >= 10:
                operation = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif 0 < mean_temp < 10:
                operation = [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            else:
                operation = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                thermal = 1460

            kWh = np.array(operation) * electric
            kWth = np.array(operation) * thermal

            for i in range(0, active_hours):
                if temp_exterior[i] < -10 and operation[i] == 1:
                    kWh[i] = kWh[i] + 2.2
                    kWth[i] = kWth[i] + 940

        return operation, cost
