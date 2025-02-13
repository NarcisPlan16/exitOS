# Class for the thermal storage + heatpump class
import os

from datetime import datetime
from Abstraction.AbsConsumer import AbsConsumer
from Abstraction.Asset_types.Consumers.ThermalStorage.HeatPump import HeatPump
from Abstraction.Asset_types.Consumers.ThermalStorage.HeatTank import HeatTank
from Abstraction.utils.utils import createClass


class ThermalStorage(AbsConsumer):

    def __init__(self, configuration, name):
        super().__init__(configuration, name)

        module_dir = os.path.basename(os.getcwd())
        if not module_dir.__contains__("Abstraction"):
            module_dir = os.path.join(module_dir, "Abstraction")
        asset_dir = os.path.join(module_dir, "Asset_types", "Consumers", "ThermalStorage")

        self.simul = createClass(asset_dir, configuration['simulate'])
        self.active_hours = configuration['active_hours']
        self.season_calendar = configuration['season_calendar']

        data = datetime.now()
        self.season = data.month.real

        self.tanks = {}
        for key in configuration['tanks']:
            self.tanks[key['name']] = HeatTank(key)

        self.pumps = {}
        for key in configuration['pumps']:
            self.pumps[key['name']] = HeatPump(key)

    def doSimula(self, **kwargs):

        calendar = kwargs['calendar']
        for pump in self.pumps.values():

            pump.config['calendar'] = []
            for hour in range(0, self.active_hours):
                power = int(calendar[hour])
                power_key_list = list(pump.partial_power.keys())
                power_key = power_key_list[power]

                pump.config['calendar'].append(power_key)

        return self.simul.simula(self=self.simul,
                                 config=self.config,
                                 tanks=self.tanks,
                                 pumps=self.pumps,
                                 season=self.season,
                                 kwargs=kwargs,
                                 kwargs_simulation=kwargs['kwargs_simulation'])

    def canviaSimula(self, simImpl):  # simImpl will be an implementation of the Simulate interface
        self.simul = simImpl

    def resetToInit(self):

        tank: HeatTank
        for tank in self.tanks.values():
            tank.reset()

        pump: HeatPump
        for pump in self.pumps.values():
            pump.reset()

    def hasTanks(self):
        return len(self.tanks) > 0

    def getTanksInfo(self):

        res_dict = {}
        for tank in self.tanks.values():
            res_dict[tank.name] = tank.actual_temperature

        return res_dict
