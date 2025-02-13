# Class for the HidrogenTank


class HidrogenTank:

    def __init__(self, configuration):
        self.config = configuration
        self.name = configuration['name']
        self.consumed_kg = 0  # Consumed kg today
        self.consumed_kg = []  # Consumed kg today hour by hour
        self.tank_max_capacity = configuration['tank_max_capacity']
        self.tank_min_capacity = configuration['tank_min_capacity']
        self.tank_initial = configuration['tank_initial']
        self.tank_under_capacity = 0  # How many hours the tank was under minimum capacity
        self.actual_capacity = configuration['tank_initial']  # Actual amount of kg stored
        self.capacity_by_hours = []  # Capacity of the tank hour by hour

    def reset(self):
        self.consumed_kg = 0  # Consumed kg today
        self.consumed_kg = []  # Consumed kg today hour by hour
        self.actual_capacity = self.tank_initial
        self.tank_under_capacity = 0  # How many hours the tank was under minimum capacity
        self.capacity_by_hours = []  # Capacity of the tank hour by hour


