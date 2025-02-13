# Class that is the parent for the different energy generators

class Generator:

    def __init__(self, configuration, name):
        self.maxWattage = configuration['max_output']
        self.minWattage = configuration['min_output']
        self.name = name
        self.config = configuration
        self.production = configuration['production']
        # Here the common attributes

    def obtainProductionByHour(self, hour):
        return self.production[hour]

    def obtainProduction(self):
        return self.production

    def obtainDailyProduction(self):
        return sum(self.production)
