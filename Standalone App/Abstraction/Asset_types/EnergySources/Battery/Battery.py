# Generic class for all types of battery
import os

from Abstraction.AbsEnergySource import AbsEnergySource
from Abstraction.utils.utils import createClass


class Battery(AbsEnergySource):

    def __init__(self, configuration, nom):

        super().__init__(configuration, nom)

        module_dir = os.path.basename(os.getcwd())
        if not module_dir.__contains__("Abstraction"):
            module_dir = os.path.join(module_dir, "Abstraction")
        asset_dir = os.path.join(module_dir, "Asset_types", "EnergySources", "Battery")

        self.potencies = []
        self.simul = createClass(asset_dir, configuration['simulate'])
        # Here common attributes between batteries

    def doSimula(self, **kwargs):
        self.config['calendar'] = kwargs['calendar']
        self.potencies = kwargs['calendar']
        return self.simul.simula(self.simul, self.config, kwargs_simulation=kwargs['kwargs_simulation'])

    def canviaSimula(self, simImpl):  # simInte will be an implementation of the Simulate interface
        self.simul = simImpl

    def resetToInit(self):
        self.potencies = []
        self.cap_actual = self.config['cap_actual']
