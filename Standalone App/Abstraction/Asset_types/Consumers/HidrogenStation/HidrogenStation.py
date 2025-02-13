# Class for the HidrogenStation consumer
import os

from Abstraction.AbsConsumer import AbsConsumer
from Abstraction.utils.utils import createClass
from Abstraction.Asset_types.Consumers.HidrogenStation.Electrolyzer import Electrolyzer
from Abstraction.Asset_types.Consumers.HidrogenStation.HidrogenTank import HidrogenTank


class HidrogenStation(AbsConsumer):

    def __init__(self, configuration, name):
        super().__init__(configuration, name)

        module_dir = os.path.basename(os.getcwd())
        if not module_dir.__contains__("Abstraction"):
            module_dir = os.path.join(module_dir, "Abstraction")
        asset_dir = os.path.join(module_dir, "Asset_types", "Consumers", "HidrogenStation")

        self.simul = createClass(asset_dir, configuration['simulate'])
        self.active_hours = configuration['active_hours']

        self.electrolyzers = {}
        for electrolyzer in configuration['electrolyzers']:
            self.electrolyzers[electrolyzer['name']] = Electrolyzer(electrolyzer)

        self.tanks = {}
        for tank in configuration['tanks']:
            self.tanks[tank['name']] = HidrogenTank(tank)

    def doSimula(self, **kwargs):

        calendar = kwargs['calendar']
        self.config["calendar"] = calendar
        for electrolyzer in self.electrolyzers.values():

            electrolyzer.config['calendar'] = []
            for hour in range(0, self.active_hours):

                power = int(calendar[hour])
                power_key_list = list(electrolyzer.partial_power.keys())
                power_key = power_key_list[power]

                electrolyzer.config['calendar'].append(power_key)
                # Rebrem valors de 0 a 5 ja que tenim 6 valors (0, 10, 20, 40, 60, 100)

        return self.simul.simula(self=self.simul,
                                 config=self.config,
                                 electrolyzers=self.electrolyzers,
                                 tanks=self.tanks,
                                 kwargs=kwargs,
                                 kwargs_simulation=kwargs['kwargs_simulation'])

    def canviaSimula(self, simImpl):  # simImpl will be an implementation of the Simulate interface
        self.simul = simImpl

    def resetToInit(self):

        elec: Electrolyzer
        for elec in self.electrolyzers.values():
            elec.reset()

        tank: HidrogenTank
        for tank in self.tanks.values():
            tank.reset()

    def hasTanks(self):
        return len(self.tanks) > 0

    def getTanksInfo(self):

        res_dict = {}
        for tank in self.tanks.values():
            res_dict[tank.name] = tank.actual_capacity

        return res_dict

    def totalStorage(self):

        res = 0
        for tank in self.tanks.values():
            res += tank.actual_capacity

        return res

    def maxCapacity(self):

        res = 0
        for tank in self.tanks.values():
            res += tank.tank_max_capacity

        return res

    def minCapacity(self):

        res = 0
        for tank in self.tanks.values():
            res += tank.tank_min_capacity

        return res

    def tankCapacityHourly(self):

        result = [0] * self.active_hours
        for tank in self.tanks.values():
            for i in range(0, self.active_hours):
                result[i] += tank.capacity_by_hours[i]

        return result
