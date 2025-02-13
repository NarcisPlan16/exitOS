# Class to represent the configuration actions

import os
import sys
import tomllib

current_dir = os.path.dirname(os.path.abspath("Configurator.py"))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

subfolder_dir = os.path.join(parent_dir, 'utils')
sys.path.append(subfolder_dir)

subfolder_dir = os.path.join(parent_dir, 'Asset_types')
sys.path.append(subfolder_dir)

from .utils import utils


class Configurator:

    def __init__(self, console):
        self.console = console

        self.assets_dir = os.getcwd()
        if self.console:
            self.assets_dir = os.path.join(self.assets_dir, "Abstraction")

    def __entrarAssets(self, llista_dir):

        for element in llista_dir:
            if element.__contains__(".toml"):
                llista_dir.remove(element)
                break

        llista = {}  # Llista amb key nom de l'asset i valor quants n'hi ha
        n_elem = 0
        for asset in llista_dir:
            if not os.path.isdir(asset):  # LListem només els directoris (assets que tenim)

                nom_asset = asset.replace(".py", "")

                print("     -> " + asset)
                print("Quants assets d'aquest tipus hi ha?")

                llista[nom_asset] = input("Entra el número: ")
                while not llista[nom_asset].isdigit():
                    llista[nom_asset] = input()
                llista[nom_asset] = int(llista[nom_asset])  # Passem el numero llegit (string) a int

                n_elem += llista[nom_asset]
                print("\n")

        return llista, n_elem  # Returns the dictionary with {key:number} and the number of total elements on the dictionary

    def __readConfigData(self, path, asset_type, lecture):

        dir = os.path.join(path, asset_type, "")

        config_path = dir + lecture + ".toml"  # path del fitxer configuració .toml
        print(config_path)
        with open(config_path, "rb") as toml:
            config_data = tomllib.load(toml)  # Llegim el fitxer
            toml.close()
            print(config_data)
            print("\n")

        return config_data  # Retornem les dades llegides

    def __configuraAsset(self, noms, path, asset_type, res):
        # Llista és una llista amb noms d'asset amb tipus asset_type

        for i in range(0, len(noms)):

            lecture = input("Entra nom del fitxer de configuració en format toml "
                            "(ex: config1) per l'asset " + asset_type + " - " + noms[i] + ": ")
            done = False
            config_data = {}
            while not done:
                try:
                    config_data = self.__readConfigData(path, asset_type, lecture)  # Llegim la configuració del .toml
                    done = True
                except tomllib.TOMLDecodeError:
                    lecture = input("Error al carregar el fitxer de configuració " + lecture +
                                    "\n Introdueix de nou el seu nom: ")
                except FileNotFoundError:
                    lecture = input("El fitxer de configuració " + lecture + " no existeix"
                                                                             "\n Introdueix de nou el seu nom: ")

            asset_path = os.path.join(path, asset_type)
            module_path = os.path.relpath(asset_path)
            classe = utils.createClass(module_path, asset_type)
            # Obtenim la classe des de l'string asset_type amb el path dels moduls
            res[noms[i]] = classe(config_data, noms[i])  # Constructor de la classe
            # Instanciem la nova classe amb la configuració i el nom, i la guardem al diccionari

        return res

    def __configure(self, noms, path):
        # Llista és un diccionari amb {key : [llista_assets]}

        res = {}
        for asset_type in noms:  # Per cada tipus d'asset al diccionari

            print("----------------Entrant configuracions per els assets de tipus " + asset_type + "----------------\n")
            res = self.__configuraAsset(noms[asset_type], path, asset_type, res)
            # Configurem tots els assets de tipus asset_type i els afegim a res

        return res

    def __entrarNoms(self, diccionari):

        noms = {}
        for asset in diccionari:

            if diccionari[asset] > 0:
                noms[asset] = []
                for n in range(0, diccionari[asset]):
                    noms[asset].append(input("Entra nom de l'asset numero " + str(n + 1) + " de tipus " + asset + ": "))

        return noms

    def initializeModels(self):

        # SETUP
        print("Benvingut al SETUP, escull quants assets de cada tipus que té el sistema. "
              "(Buildingss, Consumidors, Generadors i EnergySources).\n")

        self.assets_dir = os.path.join(self.assets_dir, "Asset_types")
        current_dir = os.getcwd()

        print("--------------------Buildings disponibles-------------------- \n")
        buildings_list = os.listdir(os.path.join(self.assets_dir, "Buildings"))
        count_buildings, n_buildings = self.__entrarAssets([buildings_list[0]])
        noms_buildings = self.__entrarNoms(count_buildings)

        print("Buildings entrats:")
        print(noms_buildings)

        print("--------------------Consumidors disponibles-------------------- \n")
        consumers_list = os.listdir(os.path.join(self.assets_dir, "Consumers"))
        count_consumers, n_consumers = self.__entrarAssets(consumers_list)
        noms_consumers = self.__entrarNoms(count_consumers)

        print("Consumidors entrats:")
        print(noms_consumers)

        print("--------------------Generadors disponibles-------------------- \n")
        generators_list = os.listdir(os.path.join(self.assets_dir, "Generators"))
        count_generators, n_generators = self.__entrarAssets(generators_list)
        noms_generators = self.__entrarNoms(count_generators)

        print("Generadors entrats:")
        print(noms_generators)

        print("--------------------EnergySources disponibles-------------------- \n")
        energy_sources_list = os.listdir(os.path.join(self.assets_dir, "EnergySources"))
        count_energy_sources, n_energy_sources = self.__entrarAssets(energy_sources_list)
        noms_sources = self.__entrarNoms(count_energy_sources)

        print("Energy Sources entrats:")
        print(noms_sources)

        print("\nTot seguit, hauràs d'escriure el nom del fitxer amb la configuració de cada asset\n")

        buildings = {}
        consumers = {}
        generators = {}
        energy_sources = {}
        if n_buildings > 0:
            buildings = self.__configure(noms_buildings, os.path.join(self.assets_dir, "Buildings"))

        if n_consumers > 0:
            consumers = self.__configure(noms_consumers, os.path.join(self.assets_dir, "Consumers"))

        if n_generators > 0:
            generators = self.__configure(noms_generators, os.path.join(self.assets_dir, "Generators"))

        if n_energy_sources > 0:
            energy_sources = self.__configure(noms_sources, os.path.join(self.assets_dir, "EnergySources"))

        return buildings, consumers, energy_sources, generators

    def configureAndCreate(self, path, asset_type, asset_config):

        asset_path = os.path.join(path, asset_type)
        module_path = os.path.relpath(asset_path)
        classe = utils.createClass(module_path, asset_type)
        # Obtenim la classe des de l'string asset_type amb el path dels moduls

        return classe(asset_config, asset_config['name'])  # Constructor de la classe
        # Instanciem la nova classe amb la configuració i el nom, i la retornem
