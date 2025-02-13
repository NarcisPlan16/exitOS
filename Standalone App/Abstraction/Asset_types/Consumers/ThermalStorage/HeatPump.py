# Class for the heat pump

class HeatPump:

    def __init__(self, configuration):
        self.name = configuration['name']
        self.max_power = configuration['max_power']
        self.efficiency = configuration['efficiency']
        self.partial_power = configuration['partial_power']
        self.config = configuration
        self.consumed_profile = []  # Perfil hora a hora de kwh consumits avui
        self.consumed_kwh = 0  # Kwh consumed today
        self.generated_heat_celcius = 0  # heat generated today

    def reset(self):
        self.consumed_profile = []
        self.consumed_kwh = 0
        self.generated_heat_celcius = 0
