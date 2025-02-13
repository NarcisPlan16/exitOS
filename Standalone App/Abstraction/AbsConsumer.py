# Interface for the Consumer entities. To abstract the simulate method so we can change it on run-time

from abc import abstractmethod


class AbsConsumer:

    def __init__(self, configuration, name):
        self.config = configuration
        self.name = name
        self.max_power = configuration['max_power']
        self.calendar_range = configuration['calendar_range']
        self.active_hours = configuration['active_hours']
        self.active_calendar = configuration['active_calendar']

        self.vbound_start = 0
        self.vbound_end = 0

    @abstractmethod
    def doSimula(self, calendar, **kwargs):
        pass

    @abstractmethod
    def resetToInit(self):
        pass

    @abstractmethod
    def hasTanks(self):
        pass
