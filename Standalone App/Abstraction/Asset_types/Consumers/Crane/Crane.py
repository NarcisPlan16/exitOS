# Class for the crane assets
import os

from Abstraction.AbsConsumer import AbsConsumer
from Abstraction.utils.utils import createClass


class Crane(AbsConsumer):

    def __init__(self, configuration, name):
        super().__init__(configuration, name)
        self.max_movements_per_hour = configuration['max_movements_per_hour']

        module_dir = os.path.basename(os.getcwd())
        if not module_dir.__contains__("Abstraction"):
            module_dir = os.path.join(module_dir, "Abstraction")
        asset_dir = os.path.join(module_dir, "Asset_types", "Consumers", "Crane")

        self.simul = createClass(asset_dir, configuration['simulate'])

    def doSimula(self, **kwargs):
        self.config['calendar'] = kwargs['calendar']
        return self.simul.simula(self.simul, self.config, kwargs_simulation=kwargs['kwargs_simulation'])

    def canviaSimula(self, simImpl):  # simInte will be an implementation of the Simulate interface
        self.simul = simImpl
