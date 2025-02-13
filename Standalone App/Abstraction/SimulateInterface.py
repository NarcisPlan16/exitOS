# Interface for the simulations

from abc import ABC, abstractmethod


class SimulateInterface(ABC):

    @abstractmethod
    def simula(self, config, **kwargs):
        # **kwargs is a dictionary with all the extra necessary arguments
        pass
