# HVac class
import os

from Abstraction.AbsConsumer import AbsConsumer
from Abstraction.utils.utils import createClass


class HVAC(AbsConsumer):

    def __init__(self, configuration, name):

        super().__init__(configuration, name)

        module_dir = os.path.basename(os.getcwd())
        if not module_dir.__contains__("Abstraction"):
            module_dir = os.path.join(module_dir, "Abstraction")
        asset_dir = os.path.join(module_dir, "Asset_types", "Consumers", "HVAC")

        self.simul = createClass(asset_dir, configuration['simulate'])

        self.temp_initial = configuration['temp_initial']

    def doSimula(self, **kwargs):
        self.config['calendar'] = kwargs['calendar']
        return self.simul.simula(self.simul, self.config, kwargs_simulation=kwargs['kwargs_simulation'])

    def canviaSimula(self, simImpl):  # simInte will be an implementation of the Simulate interface
        self.simul = simImpl
