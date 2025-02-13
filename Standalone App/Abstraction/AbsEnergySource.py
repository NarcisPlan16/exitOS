# Class that is the parent for all different energy sources

from abc import abstractmethod


class AbsEnergySource:

    def __init__(self, configuration, name):
        self.cap_actual = configuration['cap_actual']
        self.max_capacity = configuration['max_capacity']
        self.max_roc = configuration['max_roc']
        self.max_rod = configuration['max_rod']
        self.calendar_range = configuration['calendar_range']
        self.active_hours = configuration['active_hours']
        self.active_calendar = configuration['active_calendar']
        self.name = name
        self.config = configuration
        self.vbound_start = 0
        self.vbound_end = 0
        # here the common attributes between energy sources

    @abstractmethod
    def doSimula(self, calendar, **kwargs):
        pass

    @abstractmethod
    def canviaSimula(self, simImpl):
        pass

    @abstractmethod
    def resetToInit(self):
        pass
