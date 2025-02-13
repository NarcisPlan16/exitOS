# Class to represent a possible solution configuration

from AbsConsumer import AbsConsumer
from Abstraction import AbsEnergySource


class Solution:

    def __init__(self, buildings={}, consumers={}, energy_sources={}, generators={}):

        self.generators = generators
        self.consumers = consumers
        self.energy_sources = energy_sources
        self.buildings = buildings

        self.balanc_energetic_per_hores = []
        self.numero_assets_ok = 0
        self.preu_cost = 9999999999
        self.cost_aproximacio = 0
        self.temps_tardat = 0

        self.consumption_data = {}
        for building_class_list in buildings.values():
            for edifici in building_class_list.values():
                self.consumption_data[edifici.name] = edifici.obtainConsumeProfile()

        self.production_data = {}
        self.energy_sources_data = {}
        self.tanks_final_capacity = {}
        self.model_variables = []

        self.cost_per_hours = []

    def saveConsumersProfileData(self, profile):

        consumer: AbsConsumer
        profile_aux = profile
        for consumer_class in self.consumers:  # we look every class of consumer
            for consumer in self.consumers[consumer_class].keys():

                if profile_aux.__contains__(consumer):

                    self.consumption_data[consumer] = profile_aux[consumer]

                    if self.consumers[consumer_class][consumer].hasTanks():
                        self.__saveTanksInfo(self.consumers[consumer_class][consumer])

                    profile_aux.pop(consumer)  # for efficiency purposes

    def saveGeneratorsProfileData(self, profile):

        for generator in profile:
            self.production_data[generator] = profile[generator]

    def saveEnergySourcesStates(self, profile):

        for key in profile:
            self.energy_sources_data[key] = profile[key]

    def __saveTanksInfo(self, consumer):

        tanks_info = consumer.getTanksInfo()
        for tank in tanks_info:
            self.tanks_final_capacity[tank] = tanks_info[tank]

    def obtainAssetsProfiles(self):

        res_dict = {}

        for asset_class in self.consumers:
            res_dict[asset_class] = {}
            for asset in self.consumers[asset_class]:
                res_dict[asset_class][asset] = {}

                asset_data = res_dict[asset_class][asset]
                consumer: AbsConsumer
                consumer = self.consumers[asset_class][asset]

                asset_data['consumption'] = sum(self.consumption_data[asset])
                asset_data["graph_data"] = self.consumption_data[asset]
                asset_data["graph_y"] = "Consumption (kwh)"
                asset_data["graph_x"] = "Hour"
                asset_data["graph_title"] = "Consumption by hour"
                asset_data["control_variables"] = consumer.config["calendar"]

        for asset_class in self.energy_sources:
            res_dict[asset_class] = {}
            for asset in self.energy_sources[asset_class]:
                res_dict[asset_class][asset] = {}

                asset_data = res_dict[asset_class][asset]
                source: AbsEnergySource
                source = self.energy_sources[asset_class][asset]

                consumption = []
                asset_profile = self.energy_sources_data[asset]
                for hour in range(len(asset_profile) - 1):
                    consumption.append(asset_profile[hour] - asset_profile[hour + 1])

                asset_data['consumption'] = sum(consumption)
                asset_data["graph_data"] = asset_profile
                asset_data["graph_y"] = "Battery capacity"
                asset_data["graph_x"] = "Hour"
                asset_data["graph_title"] = "Battery capacity over time"
                asset_data["control_variables"] = source.config["calendar"]

        return res_dict
