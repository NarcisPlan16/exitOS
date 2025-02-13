# Class for the heat tank

class HeatTank:

    def __init__(self, configuration):
        self.name = configuration['name']
        self.config = configuration
        self.actual_temperature = configuration['tank_initial']  # Actual temperature
        self.initial_temperature = configuration['tank_initial']  # initial temperature
        self.min_temperature = configuration['tank_min']
        self.max_temperature = configuration['tank_max']

    def reset(self):
        self.actual_temperature = self.initial_temperature

