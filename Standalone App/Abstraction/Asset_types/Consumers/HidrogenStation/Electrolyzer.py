# Electrolyzer class


class Electrolyzer:

    def __init__(self, configuration):
        self.name = configuration['name']
        self.generated_kg = 0  # kg generated today
        self.consumed_kwh = 0  # Kwh consumed today
        self.consumed_profile = []  # Perfil hora a hora de kwh consumits avui
        self.primer_cop = True
        self.tank_under_capacity = 0
        self.conversion_ratio = configuration['conversion_ratio']
        self.partial_power = configuration['partial_power']
        self.config = configuration

    def reset(self):
        self.generated_kg = 0  # kg generated today
        self.consumed_kwh = 0  # Kwh consumed today
        self.consumed_profile = []  # Perfil hora a hora de kwh consumits avui
        self.primer_cop = True
        self.tank_under_capacity = 0
