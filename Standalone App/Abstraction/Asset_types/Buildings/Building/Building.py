# class to represent a building consumer


class Building:

    def __init__(self, configuration, name):
        self.name = name
        self.config = configuration

    def obtainConsumeByHour(self, hour):
        return self.config['consume_profile'][hour]

    def obtainDailyConsume(self):
        return sum(self.config['consume_profile'])

    def obtainConsumeProfile(self):
        return self.config['consume_profile']
