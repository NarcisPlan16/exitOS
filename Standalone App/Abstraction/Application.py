import json
import time
import os
import ast
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import tomllib

import PIL.Image
import customtkinter
from matplotlib import pyplot as plt

import Solution as solution
from Abstraction.utils import utils

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


class Application(customtkinter.CTk):

    def __init__(self, opt_scheduler, simulation_event):

        super().__init__()

        # initialize OS
        self.optimal_scheduler = opt_scheduler

        # Configure window
        self.title("Optimal Scheduler")
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        self.geometry(str(int(width/1.25)) + "x" + str(int(height/1.35)))  # width x height + x + y, x i y serveixen per dir on apareix la window

        # configure grid layout (8x3)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(8, weight=1)

        self.__initSideMenu()

        self.simulation_event = simulation_event

        # Create main view
        self.main_view = customtkinter.CTkFrame(self, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.main_view.grid(row=0, column=1, rowspan=9, columnspan=3, sticky="nsew")
        self.main_view.grid_columnconfigure((0,1,2,3), weight=1)
        self.main_view.grid_rowconfigure((0,1,2,3), weight=1)

        self.welcome_text = customtkinter.CTkLabel(self.main_view, text="Welcome to the Optimal Scheduler Setup",
                                                   font=customtkinter.CTkFont(size=28, weight="bold"))
        self.welcome_text.grid(row=1, column=1, padx=(60, 0), pady=(50, 50), sticky="nsew")

        self.welcome_text = customtkinter.CTkLabel(self.main_view,
                                                   text="On your left there is the menu where you can change which "
                                                        "type of assets are you adding to the system and "
                                                        "add its configurations",
                                                   font=customtkinter.CTkFont(size=15, weight="normal"), wraplength=700)
        self.welcome_text.grid(row=2, column=1, padx=(60, 0), pady=(30, 180), sticky="nsew")


    def __initSideMenu(self):

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=9, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        # Add widgets to the side_bar
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Option menu",
                                                  font=customtkinter.CTkFont(size=19, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(40, 40), sticky="nsew", ipady=10, ipadx=40)

        # Buildings button
        self.buildings_btn = customtkinter.CTkButton(self.sidebar_frame, text="Buildings",
                                                     command=lambda: self.__displayAssetType("Buildings"),
                                                     font=customtkinter.CTkFont(size=16, weight="normal"),
                                                     corner_radius=0)
        self.buildings_btn.grid(row=1, column=0, padx=0, pady=2, sticky="nsew", ipady=8)

        # Consumers button
        self.consumers_btn = customtkinter.CTkButton(self.sidebar_frame, text="Consumers",
                                                     command=lambda: self.__displayAssetType("Consumers"),
                                                     font=customtkinter.CTkFont(size=16, weight="normal"),
                                                     corner_radius=0)
        self.consumers_btn.grid(row=2, column=0, padx=0, pady=2, sticky="nsew", ipady=8)

        # Energy Sources button
        self.esouces_btn = customtkinter.CTkButton(self.sidebar_frame, text="Energy Sources",
                                                   command=lambda: self.__displayAssetType("EnergySources"),
                                                   font=customtkinter.CTkFont(size=16, weight="normal"),
                                                   corner_radius=0)
        self.esouces_btn.grid(row=3, column=0, padx=0, pady=2, sticky="nsew", ipady=8)

        # Generators button
        self.generators_btn = customtkinter.CTkButton(self.sidebar_frame, text="Generators",
                                                      command=lambda: self.__displayAssetType("Generators"),
                                                      font=customtkinter.CTkFont(size=16, weight="normal"),
                                                      corner_radius=0)
        self.generators_btn.grid(row=4, column=0, padx=0, pady=2, sticky="nsew", ipady=8)

        # Electricity prices button
        self.overview_btn = customtkinter.CTkButton(self.sidebar_frame, text="Electricity prices", command=self.__changeElectricityPrices,
                                                    font=customtkinter.CTkFont(size=16, weight="normal"),
                                                    corner_radius=0)
        self.overview_btn.grid(row=5, column=0, padx=0, pady=(50, 2), sticky="new", ipady=8)

        # Global overview button
        self.overview_btn = customtkinter.CTkButton(self.sidebar_frame, text="Overview", command=self.__showOverview,
                                                      font=customtkinter.CTkFont(size=16, weight="normal"),
                                                      corner_radius=0)
        self.overview_btn.grid(row=6, column=0, padx=0, pady=(2, 2), sticky="new", ipady=8)

        # Boto run
        current_dir = os.getcwd()
        if self.optimal_scheduler.console_debug:
            current_dir = os.path.join(current_dir, "Abstraction")

        img_dir = os.path.join(current_dir, "img", "Run.png")
        img = PIL.Image.open(img_dir)
        photo = customtkinter.CTkImage(dark_image=img, size=(40, 40))  # Creating image

        # Run simulation button
        self.run_btn = customtkinter.CTkButton(self.sidebar_frame, text="Run Simulation", command=self.__runSimulation,
                                               font=customtkinter.CTkFont(size=16, weight="normal"),
                                               corner_radius=14, image=photo, compound=customtkinter.RIGHT)
        self.run_btn.grid(row=9, column=0, padx=0, pady=20, ipady=4)

    def __changeElectricityPrices(self):

        for widget in self.main_view.winfo_children():
            widget.destroy()

        frame = customtkinter.CTkScrollableFrame(self.main_view, corner_radius=16)
        frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew", columnspan=4, rowspan=4)
        frame.columnconfigure((0,1,2,3,4), weight=1)

        title = customtkinter.CTkLabel(frame, text="Electricity prices",
                                       font=customtkinter.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=2, padx=(200, 0), pady=(25, 10), sticky="nsew")

        frame_buy = customtkinter.CTkFrame(frame, corner_radius=0, bg_color="transparent", fg_color="transparent")
        frame_buy.grid(row=1, column=2, padx=(0, 0), pady=(80, 0), sticky="nsew", columnspan=2, rowspan=1)
        buy_prices = FeatureInputFrame(frame_buy, "Buy prices (€)", 0, 0, 2, [24], None)

        frame_sell = customtkinter.CTkFrame(frame, corner_radius=0, bg_color="transparent", fg_color="transparent")
        frame_sell.grid(row=2, column=2, padx=(0, 0), pady=(30, 0), sticky="nsew", columnspan=2, rowspan=1)
        sell_prices = FeatureInputFrame(frame_sell, "Sell prices (€)", 0, 1, 2, [24], None)

        i = 0
        for child in buy_prices.feature_entry_frame.winfo_children():
            if child.__class__.__name__ == "CTkEntry":
                child.delete(0, "end")  # Clear the existing text
                child.insert(0, self.optimal_scheduler.electricity_prices[i])
                i += 1

        i = 0
        for child in sell_prices.feature_entry_frame.winfo_children():
            if child.__class__.__name__ == "CTkEntry":
                child.delete(0, "end")  # Clear the existing text
                child.insert(0, self.optimal_scheduler.electricity_sell_prices[i])
                i += 1

        set_btn = customtkinter.CTkButton(frame, text="Save prices",
                                          command=lambda: self.__savePrices(sell_prices, buy_prices),
                                          font=customtkinter.CTkFont(size=18, weight="normal"),
                                          corner_radius=14)
        set_btn.grid(row=4, column=2, sticky="ns", padx=(0, 0), pady=(50, 0), ipady=10, ipadx=50)

    def __savePrices(self, sell_frame, buy_frame):

        try:
            sell_prices_list = self.__getFeatureEntries(sell_frame.feature_entry_frame, "Sell prices (€)")
            buy_prices_list = self.__getFeatureEntries(buy_frame.feature_entry_frame, "Buy prices (€)")

            self.optimal_scheduler.savePrices(sell_prices_list, buy_prices_list)
        except ValueError:

            popup = self.createPopup("Error", "Some values are empty and must be specified")
            popup.mainloop()

    def __showOverview(self):

        for widget in self.main_view.winfo_children():
            widget.destroy()

        overview_title = customtkinter.CTkLabel(self.main_view, text="Assets Overview",
                                                font=customtkinter.CTkFont(size=28, weight="bold"))
        overview_title.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew", columnspan=2)

        assets_dict = self.optimal_scheduler.obtainAssetsInfo()
        assets_frame = AssetsFrame(self.main_view, assets_dict, self)
        assets_frame.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew", rowspan=4, columnspan=4)

    def saveConfiguration(self):

        current_dir = os.getcwd()
        if self.optimal_scheduler.console_debug:
            current_dir = os.path.join(current_dir, "Abstraction")
        save_dir = os.path.join(current_dir, "SavedOSConfigs")

        files = [('Json Files', '*.json')]
        file = fd.asksaveasfile(filetypes=files, defaultextension="json", initialdir=save_dir)

        self.optimal_scheduler.saveAssetsConfigurationInfo(file.name)

        popup = self.createPopup("Saved successfully", "File saved successfully")
        popup.mainloop()

    def importConfiguration(self):

        current_dir = os.getcwd()
        if self.optimal_scheduler.console_debug:
            current_dir = os.path.join(current_dir, "Abstraction")
        save_dir = os.path.join(current_dir, "SavedOSConfigs")

        files = [('Json Files', '*.json')]
        file = fd.askopenfile(filetypes=files, initialdir=save_dir, defaultextension="json")

        config = json.load(file)
        self.optimal_scheduler.deleteAssets()

        for asset_type in config:

            if asset_type == "electricity_prices":
                self.optimal_scheduler.electricity_prices = config[asset_type]
            elif asset_type == "electricity_sell_prices":
                self.optimal_scheduler.electricity_sell_prices = config[asset_type]
            else:
                for asset_class in config[asset_type]:
                    for asset in config[asset_type][asset_class].values():
                        self.optimal_scheduler.addAsset(asset_type, asset_class, asset)

        # if not "electricity_prices" in config and not "electricity_sell_prices" in config:
        # popup = self.createPopup("Info", "No electricity prices found in the configuration file, default prices are loaded")
        # popup.mainloop()

        self.__showOverview()

    def __displayAssetType(self, type):

        self.folder = type

        for widget in self.main_view.winfo_children():
            widget.destroy()

        self.enter_frame = SelectFrame(self.main_view, type)
        self.enter_frame.grid(row=0, column=0, padx=(20, 20), pady=(40, 0), sticky="wn", ipadx=25, ipady=30)

    def updateProgress(self, read_pipe):

        iterations, maxiter, = read_pipe.recv()
        self.progress_bar.set(iterations/maxiter)
        self.step_text.configure(text="Step " + str(iterations) + "/" + str(maxiter))

        done = False
        while iterations < maxiter and not done:

            if read_pipe.poll():

                iterations, maxiter, = read_pipe.recv()

                if iterations == -1:
                    done = True
                else:
                    self.progress_bar.set(iterations / maxiter)
                    self.step_text.configure(text="Step " + str(iterations) + "/" + str(maxiter))

            else:
                time.sleep(0.5)

        self.progress_bar.set(1)
        self.step_text.configure(text="Step " + str(maxiter) + "/" + str(maxiter))
        time.sleep(1.5)
        for widget in self.main_view.winfo_children():
                widget.destroy()

        while read_pipe.poll():
            solucio = read_pipe.recv()

        read_pipe.close()
        self.simulation_event.clear()

        self.__displaySimulationResults(solucio)

    def __displaySimulationResults(self, solucio: solution.Solution):

        current_dir = os.getcwd()
        if self.optimal_scheduler.console_debug:
            current_dir = os.path.join(current_dir, "Abstraction")
        img_dir = os.path.join(current_dir, "result_imgs", "cost.png")

        img = PIL.Image.open(img_dir)
        img_size = (int(img.size[0] * 0.35), int(img.size[1] * 0.35))
        photo = customtkinter.CTkImage(dark_image=img, size=img_size)  # Creating image

        result_frame = customtkinter.CTkScrollableFrame(self.main_view, corner_radius=16)
        result_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew", columnspan=4, rowspan=4)
        result_frame.grid_columnconfigure((0,1), weight=1)

        title = customtkinter.CTkLabel(result_frame, text="Simulation results",
                                       font=customtkinter.CTkFont(size=25, weight="bold"))
        title.grid(row=0, column=0, padx=(0, 0), pady=(10, 30), sticky="nsew", columnspan=2)

        general_frame = customtkinter.CTkFrame(result_frame, corner_radius=16)
        general_frame.grid(row=1, column=0, padx=(10, 10), pady=(25, 25), sticky="nsew", columnspan=2)
        general_frame.grid_columnconfigure((0, 1), weight=1)

        photo_label = customtkinter.CTkLabel(general_frame, text="", image=photo)
        photo_label.grid(row=0, column=0, padx=(0, 10), pady=(0, 10))

        stats_frame = customtkinter.CTkFrame(general_frame, corner_radius=16)
        stats_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.__displaySolutionMetrics(solucio, stats_frame)
        self.__displayAssetsVariables(solucio, result_frame, 2)

    def __displaySolutionMetrics(self, solucio, stats_frame):

        cost_label = customtkinter.CTkLabel(stats_frame, text="Cost:  " + str(round(solucio.preu_cost, 4)) + "€",
                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        cost_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsw")

        aproximation_cost_label = customtkinter.CTkLabel(stats_frame,
                                                         text="Cost d'aproximació:  " +
                                                              str(round(solucio.cost_aproximacio, 4)),
                                                         font=customtkinter.CTkFont(size=16, weight="bold"))
        aproximation_cost_label.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsw")

        spent_time_label = customtkinter.CTkLabel(stats_frame,
                                                  text="Temps tardat:  " + str(round(solucio.temps_tardat, 4)) + "s",
                                                  font=customtkinter.CTkFont(size=16, weight="bold"))
        spent_time_label.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="nsw")

        model_variables = customtkinter.CTkLabel(stats_frame,
                                                 text="Model variables:  " + str(solucio.model_variables),
                                                 font=customtkinter.CTkFont(size=16, weight="bold"),
                                                 wraplength=400)
        model_variables.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="nsw")

    def __displayAssetsVariables(self, solucio, frame, fila):

        asset_dict = solucio.obtainAssetsProfiles()
        for asset_class in asset_dict:
            for asset in asset_dict[asset_class]:

                asset_frame = customtkinter.CTkFrame(frame, corner_radius=16)
                asset_frame.grid(row=fila, column=0, padx=(10, 10), pady=(25, 25), sticky="nsew", columnspan=2)
                asset_frame.grid_columnconfigure((0,1), weight=1)

                title = customtkinter.CTkLabel(asset_frame, text=asset_class + " - " + asset,
                                               font=customtkinter.CTkFont(size=16, weight="bold"))
                title.grid(row=0, column=0, padx=(0, 0), pady=(10, 30), sticky="nsew", columnspan=2)

                self.__displayAssetData(asset_dict[asset_class][asset], asset, asset_frame)

                fila += 1

    def __displayAssetData(self, data_dict, asset, frame):

        plt.plot(data_dict["graph_data"])
        plt.xlabel(data_dict['graph_x'])
        plt.ylabel(data_dict['graph_y'])
        plt.title(data_dict['graph_title'])
        fig1 = plt.gcf()

        current_dir = os.getcwd()
        if self.optimal_scheduler.console_debug:
            current_dir = os.path.join(current_dir, "Abstraction")
        img_dir = os.path.join(current_dir, "result_imgs", asset + ".png")
        fig1.savefig(img_dir, dpi=200)
        plt.close(fig1)

        img = PIL.Image.open(img_dir)
        img_size = (int(img.size[0] * 0.4), int(img.size[1] * 0.4))
        photo = customtkinter.CTkImage(dark_image=img, size=img_size)  # Creating image
        photo_label = customtkinter.CTkLabel(frame, text="", image=photo)
        photo_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

        stats_frame = customtkinter.CTkFrame(frame, corner_radius=16)
        stats_frame.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        total_consumption = data_dict["consumption"]
        consumption_title = customtkinter.CTkLabel(stats_frame,
                                                   text="Total consumption:  " + str(total_consumption) + " Kwh",
                                                   font=customtkinter.CTkFont(size=16, weight="bold"),
                                                   wraplength=400)
        consumption_title.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="nsw")

        calendar_label = customtkinter.CTkLabel(stats_frame,
                                                text="Control Variables:  " + str(data_dict["control_variables"]),
                                                font=customtkinter.CTkFont(size=16, weight="bold"),
                                                wraplength=400)
        calendar_label.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsw")

        # do a loop here to diplay other info if tehere is

    def __runSimulation(self):

        for widget in self.main_view.winfo_children():
                widget.destroy()

        self.progress_text = customtkinter.CTkLabel(self.main_view, text="Running simulation...",
                                                   font=customtkinter.CTkFont(size=28, weight="bold"))
        self.progress_text.grid(row=0, column=1, padx=(100, 0), pady=(170, 10), sticky="nsew")

        self.step_text = customtkinter.CTkLabel(self.main_view, text="Step 0/" + str(self.optimal_scheduler.maxiter),
                                                font=customtkinter.CTkFont(size=18, weight="normal"))
        self.step_text.grid(row=1, column=1, padx=(100, 0), pady=(70, 20), sticky="s")

        self.progress_bar = customtkinter.CTkProgressBar(self.main_view)
        self.progress_bar.grid(row=2, column=1, padx=(100, 0), pady=(0, 0), ipadx=150, sticky="n")
        self.progress_bar.set(0)

        self.simulation_event.set()

    def __importAssetConfig(self):

        file_types = (('Toml files', '*.toml'), ('All files', '*.*'))

        filename = fd.askopenfilename(title='Open a file', initialdir=os.curdir, filetypes=file_types)
        showinfo(title='Selected File', message=filename)

        with open(filename, "rb") as toml:
            config_data = tomllib.load(toml)  # Llegim el fitxer
            toml.close()

        for frame in self.config_frame.winfo_children():
            frame.destroy()

        self.displayAssetConfig(self.selected_asset, config_data)

    def displayAssetConfig(self, selection, config=None):

        self.selected_asset = selection
        self.add_asset_btn = customtkinter.CTkButton(self.main_view, corner_radius=16, text="Add asset",
                                                     command=self.__addAsset,
                                                     font=customtkinter.CTkFont(size=16, weight="normal"))
        self.add_asset_btn.grid(row=0, column=2, padx=(0, 20), pady=(0, 60), ipady=15, sticky="ew")

        self.import_config_btn = customtkinter.CTkButton(self.main_view, corner_radius=16, text="Import asset config",
                                                         command=self.__importAssetConfig,
                                                         font=customtkinter.CTkFont(size=16, weight="normal"))
        self.import_config_btn.grid(row=0, column=3, padx=(20, 70), pady=(0, 60), ipady=15, sticky="ew")

        self.config_frame = ConfigFrame(self.main_view, self.folder, selection, config)
        self.config_frame.grid(row=1, column=0, padx=(20, 20), pady=(0, 0), rowspan=4, columnspan=4, sticky="nsew")

    def __addAsset(self):

        try:
            attributes_dict = {}
            asset_frame: customtkinter.CTkFrame
            for asset_frame in self.config_frame.winfo_children():

                attribute_name = ""
                if not isinstance(asset_frame, customtkinter.CTkButton):

                    attributes_dict.update(self.__readFeatures(asset_frame, attribute_name))

            try:

                self.optimal_scheduler.addAsset(self.folder, self.selected_asset, attributes_dict)

                popup = self.createPopup("Asset added", "Asset added to simulation")
                popup.mainloop()

            except KeyError:

                popup = self.createPopup("Error", "Hi ha hagut un error al afegir l'asset")
                popup.mainloop()

            except TypeError:

                popup = self.createPopup("Error", "Hi ha algun camp buit que no pot estar-ho, com per exemple "
                                                  "el camp SIMULATE, que ha de tenir el nom del fitxer de simulació")
                popup.mainloop()

            except ModuleNotFoundError:

                popup = self.createPopup("Error", "No existeix el fitxer de simulació especificat")
                popup.mainloop()

        except ValueError:
            popup = self.createPopup("Error", "You must specify a name and a simulate file")
            popup.mainloop()

    def __readFeatures(self, asset_frame, attribute_name):

        attributes_dict = {}
        for child in asset_frame.winfo_children():

            if self.__noLabel(asset_frame) and not isinstance(child, customtkinter.CTkButton):
                # Means that is an added feature
                entries = self.__getFeatureEntries(child, attribute_name)
                attributes_dict[entries[0]] = entries[1:]
            elif not isinstance(child, customtkinter.CTkButton):

                if child.__class__.__name__ == "CTkLabel":
                    attribute_name = child.cget("text")
                else:
                    entry = self.__getFeatureEntries(child, attribute_name)
                    entry = self.__formatEntry(entry)
                    attributes_dict[attribute_name] = entry

        return attributes_dict

    def createPopup(self, title, content):

        popup = customtkinter.CTk()
        popup.wm_title(title)
        popup.geometry("400x150+500+400")
        label = customtkinter.CTkLabel(popup, text=content,
                                       font=customtkinter.CTkFont(size=16, weight="normal"),
                                       wraplength=350)
        label.pack(anchor="center", fill="x", pady=20, padx=10)
        btn = customtkinter.CTkButton(popup, text="Okay", command=popup.destroy)
        btn.pack(pady=10)

        return popup

    def __formatEntry(self, entry):

        res = entry
        if isinstance(entry, str):
            try:
                res = float(entry)
            except ValueError:
                pass

        if "{" and "}" in str(entry):  # means we have a dictionary or list of entries
            res = self.__convertToArrayOrDict(entry)

        return res

    def __convertToArrayOrDict(self, entry):

        array_res = []

        if not isinstance(entry, list) or isinstance(entry, str):

            res = ast.literal_eval(entry)
            array_res = res
        else:
            array_res = entry

        return array_res

    def __noLabel(self, frame: customtkinter.CTkFrame):

        res = True
        for child in frame.winfo_children():
            if isinstance(child, customtkinter.CTkLabel):
                res = False
                break

        return res

    def __getFeatureEntries(self, frame: customtkinter.CTkFrame, attribute_name):

        entries = []
        for child in frame.winfo_children():

            if child.__class__.__name__ == "CTkEntry":

                value = child.get()
                if value == '' and attribute_name != "name" and attribute_name != "simulate":
                    value = 0
                elif value == '' and (attribute_name == "name" or attribute_name == "simulate"):
                    raise ValueError
                elif utils.isNumber(value):
                    value = utils.toNumber(value)

                entries.append(value)

        if len(entries) == 1:
            return entries[0]
        else:
            return entries


class ConfigFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, class_folder, asset_folder, config):
        super().__init__(master, corner_radius=16)

        # fg_color="transparent"

        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.class_folder = class_folder
        self.asset_folder = asset_folder

        self.__displayInputsConfig(config)

    def __displayInputsConfig(self, config):

        if config is None:

            current_dir = os.getcwd()

            asset_dir = os.path.join(current_dir, "Asset_types", self.class_folder, str(self.class_folder) + ".toml")
            with open(asset_dir, "rb") as toml:
                config_data = tomllib.load(toml)  # Llegim el fitxer
                toml.close()

            asset_dir = os.path.join(current_dir, "Asset_types", self.class_folder, self.asset_folder, str(self.asset_folder) + ".toml")
            with open(asset_dir, "rb") as toml:
                config_data_asset = tomllib.load(toml)  # Llegim el fitxer
                toml.close()

            config_data.update(config_data_asset)

        else:
            config_data = config

        row = 0
        column = 0
        column, row = self.__displayFeatureInput("name", 1, row, column)
        for feature in config_data:

            if config is not None:
                config_value = config[feature]
            else:
                config_value = config

            column, row = self.__displayFeatureInput(feature, config_data[feature], row, column, config_value)

            if column >= 3:
                row += 1
                column = 0

        self.__addNewFeatureButton(row, column)

    def __displayFeatureInput(self, feature, value, row, column, read=None):

        columna = column
        fila = row

        colspan = 1
        if read is not None:
            if isinstance(value, list) and not isinstance(value, str):
                colspan = 3
        elif isinstance(value, list):
            colspan = value[0]

        feature_frame = FeatureInputFrame(self, feature, columna, fila, colspan, value, read)
        columna += 1

        if colspan > 1:  # we have a list

            columna = 0
            fila = row + 2

        return columna, fila

    def __addNewFeatureButton(self, row, column):

        self.add_new_feature_btn = customtkinter.CTkButton(self, corner_radius=16,
                                                           text="Add attribute",
                                                           command=lambda: self.__displayNewFeatureSelector(row, column),
                                                           font=customtkinter.CTkFont(size=16, weight="normal"))
        self.add_new_feature_btn.grid(row=row, column=column, padx=(5, 0), pady=(0, 10), ipady=15, ipadx=40)

    def __displayNewFeatureSelector(self, row, column):

        self.add_new_feature_btn.destroy()

        self.feature_selector = customtkinter.CTkOptionMenu(self,
                                                            values=['List', 'Dictionary: List of key - value', 'Single Value'],
                                                            command=self.__addNewFeatureFrame,
                                                            anchor=customtkinter.CENTER,
                                                            font=customtkinter.CTkFont(size=14, weight="normal"),
                                                            dropdown_font=customtkinter.CTkFont(size=14, weight="normal"),
                                                            dynamic_resizing=True,
                                                            width=200)
        self.feature_selector.grid(row=row, column=column, padx=(10, 10), pady=(10, 10), columnspan=1)

    def __addNewFeatureFrame(self, selection):

        column = self.feature_selector.grid_info().keys().mapping['column']
        row = self.feature_selector.grid_info().keys().mapping['row']
        self.feature_selector.destroy()

        add_new_feature_frame = customtkinter.CTkFrame(self, corner_radius=12)
        add_new_feature_frame.grid(row=row, column=column, sticky="nsew",
                                   ipady=10, pady=(10, 10), padx=(10, 10))
        add_new_feature_frame.grid_rowconfigure((0, 1), weight=1)
        add_new_feature_frame.grid_columnconfigure(0, weight=1)

        feature_values_frame = customtkinter.CTkFrame(add_new_feature_frame, corner_radius=12,
                                                      fg_color="transparent")
        feature_values_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        feature_values_frame.grid_rowconfigure((0, 1, 2), weight=1)
        feature_values_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)

        entry_name = customtkinter.CTkEntry(feature_values_frame, placeholder_text="attribute name",
                                            height=30)
        entry_name.grid(row=0, column=0, padx=(10, 10), pady=(15, 10), sticky="ew")

        self.new_feature_fila = 0
        self.new_feature_columna = 1

        if selection == "List":
            row += 1
            column = 0
            add_new_feature_frame.grid(row=row, column=0, columnspan=3)
            add_entry_btn = customtkinter.CTkButton(feature_values_frame.master, corner_radius=16,
                                                    command=lambda: self.__addNewEntry(feature_values_frame, "LIST"),
                                                    text="Add field")
            add_entry_btn.grid(column=0, row=1, padx=(5, 0), pady=(10, 10), columnspan=3)
            row += 1

        elif selection == "Dictionary: List of key - value":
            row += 1
            column = 0
            add_new_feature_frame.grid(row=row, column=0, columnspan=3)
            add_entry_btn = customtkinter.CTkButton(feature_values_frame.master, corner_radius=16,
                                                    command=lambda: self.__addNewEntry(feature_values_frame, "DICT"),
                                                    text="Add field")
            add_entry_btn.grid(column=0, row=1, padx=(5, 0), pady=(10, 10), columnspan=3)
            row += 1
        else:
            entry_value = customtkinter.CTkEntry(feature_values_frame, placeholder_text="0", width=40)
            entry_value.grid(row=self.new_feature_fila, column=self.new_feature_columna+1, sticky="ew", padx=(5, 0),
                             pady=(10, 5))
            column += 1

        if column >= 3:
            column = 0
            row += 1

        self.__addNewFeatureButton(row, column)

    def __addNewEntry(self, feature_values_frame, selection):

        entry = customtkinter.CTkEntry(feature_values_frame, placeholder_text="0", width=40)
        entry.grid(row=self.new_feature_fila, column=self.new_feature_columna, sticky="ew", padx=(5, 0), pady=(10, 10))

        if selection == "LIST":
            self.new_feature_columna += 1
            if self.new_feature_columna > 12:
                self.new_feature_fila += 1
                self.new_feature_columna = 1
        elif selection == "DICT":

            key_text = customtkinter.CTkLabel(feature_values_frame, text="Key",
                                              font=customtkinter.CTkFont(size=14, weight="normal"))
            key_text.grid(row=self.new_feature_fila + 1, column=self.new_feature_columna)

            entry_value = customtkinter.CTkEntry(feature_values_frame, placeholder_text="0", width=40)
            entry_value.grid(row=self.new_feature_fila + 2, column=self.new_feature_columna, sticky="ew", padx=(5, 0),
                       pady=(10, 5))

            value_text = customtkinter.CTkLabel(feature_values_frame, text="Value",
                                              font=customtkinter.CTkFont(size=14, weight="normal"))
            value_text.grid(row=self.new_feature_fila + 3, column=self.new_feature_columna)

            self.new_feature_columna += 1
            if self.new_feature_columna > 12:
                self.new_feature_columna = 1
                self.new_feature_fila += 4


class FeatureInputFrame(customtkinter.CTkFrame):

    def __init__(self, master, feature, columna, fila, columnspan, value, read):

        super().__init__(master)

        self.feature_frame = customtkinter.CTkFrame(self.master, corner_radius=12)  # fg_color="#3d3d3d"
        self.feature_frame.grid(row=fila, column=columna, sticky="nsew", ipadx=10, ipady=10, pady=(10, 10), padx=(10, 10))

        self.feature_title = customtkinter.CTkLabel(self.feature_frame, text=feature,
                                                    font=customtkinter.CTkFont(size=16, weight="normal"))
        self.feature_title.grid(row=0, column=0, padx=(20, 30), pady=(15, 0), sticky="snew")

        self.feature_entry_frame = customtkinter.CTkFrame(self.feature_frame, corner_radius=0,
                                                     bg_color="transparent", fg_color="transparent")
        self.feature_entry_frame.grid(row=0, column=1, rowspan=1, columnspan=columnspan, sticky="nsew")

        self.__displayInput(columnspan, fila, value, read)

    def __displayInput(self, colspan, fila, value, read):

        if colspan > 1:  # we have a list

            self.feature_frame.grid(columnspan=3, row=fila+1, column=0)

            if read is None:
                rang = value[0]
            else:
                rang = len(value)

            for hour in range(0, rang):

                feature_index = customtkinter.CTkLabel(self.feature_entry_frame, text=str(hour) + "h",
                                                       font=customtkinter.CTkFont(size=14, weight="normal"))
                self.feature_entry = customtkinter.CTkEntry(self.feature_entry_frame, placeholder_text="0", width=50)

                if hour >= 12:
                    feature_index.grid(row=2, column=hour - 12, sticky="nsew", padx=(5, 0), pady=(10, 0))
                    self.feature_entry.grid(row=3, column=hour - 12, sticky="ns", padx=(5, 0), pady=(0, 0))
                else:
                    feature_index.grid(row=0, column=hour, sticky="nsew", padx=(5, 0), pady=(10, 0))
                    self.feature_entry.grid(row=1, column=hour, sticky="ns", padx=(5, 0), pady=(0, 10))

                if read is not None:
                    self.feature_entry.insert(0, read[hour])

        else:

            self.feature_entry_frame.grid_columnconfigure(0, weight=1)
            self.feature_entry_frame.grid_rowconfigure(0, weight=1)

            self.feature = customtkinter.CTkEntry(self.feature_entry_frame, placeholder_text="0", width=80)
            self.feature.grid(row=0, column=0, sticky="sew", padx=(25, 10), pady=(32, 0))
            self.feature_title.grid(pady=(32, 0))

            if read is not None:
                self.feature.insert(0, read)


class AssetsFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, assets_info, app):
        super().__init__(master)

        self.app = app
        self.assets_info = assets_info
        self.grid_columnconfigure(0, weight=1)

        self.__displayAssetsInfo(assets_info)

    def __displayAssetsInfo(self, assets_info):

        fila = 1
        empty = True
        for asset_type in assets_info.keys():  # For every type of asset (Consumer, generator...)

            asset_type_frame = customtkinter.CTkFrame(self, corner_radius=0)
            asset_type_frame.grid(row=fila, column=0, padx=(20, 10), pady=(10, 40), sticky="nsew")

            if (asset_type == "Consumers" or asset_type == "EnergySources") and len(assets_info[asset_type].keys()) > 0:
                # TODO: REMOVE (IMPROVE)
                self.__fillAssetTypeFrameColTitles(asset_type_frame)

            added = False
            for asset_class in assets_info[asset_type].keys():  # For every asset of this type

                for asset_key in assets_info[asset_type][asset_class].keys():
                    self.__fillAssetFrame(asset_key,
                                          assets_info[asset_type][asset_class][asset_key],
                                          asset_class,
                                          asset_type_frame, fila)

                    fila += 1
                    added = True

            if added:
                asset_type_title = customtkinter.CTkLabel(asset_type_frame, text=asset_type,
                                                          font=customtkinter.CTkFont(size=18, weight="normal"),
                                                          width=100)
                asset_type_title.grid(row=1, rowspan=fila, column=0, sticky="nsew", padx=(10, 20), pady=(10, 10))

                empty = False
            else:
                empty = True and empty
                asset_type_frame.destroy()

        if empty:

            no_assets_text = customtkinter.CTkLabel(self, text="There are no assets added",
                                                    font=customtkinter.CTkFont(size=18, weight="normal"),
                                                    wraplength=700)
            no_assets_text.grid(row=0, column=0, padx=(0, 0), pady=(110, 10), sticky="nsew")

            import_config_btn = customtkinter.CTkButton(self, text="Import configuration",
                                                        command=self.app.importConfiguration,
                                                        font=customtkinter.CTkFont(size=18, weight="normal"),
                                                        corner_radius=14)
            import_config_btn.grid(row=1, column=0, sticky="ns", ipadx=14, ipady=8, padx=(0, 0), pady=(80, 0))

        else:

            btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            btn_frame.grid(row=fila, column=0, sticky="nsew", padx=(0, 0), pady=(0, 0))
            btn_frame.grid_columnconfigure((0,1), weight=1)

            save_config_btn = customtkinter.CTkButton(btn_frame, text="Save configuration",
                                                      command=self.app.saveConfiguration,
                                                      font=customtkinter.CTkFont(size=18, weight="normal"),
                                                      corner_radius=14)
            save_config_btn.grid(row=0, column=0, sticky="nse", ipadx=14, ipady=8, padx=(0, 10), pady=(0, 0))

            import_config_btn = customtkinter.CTkButton(btn_frame, text="Import configuration",
                                                        command=self.app.importConfiguration,
                                                        font=customtkinter.CTkFont(size=18, weight="normal"),
                                                        corner_radius=14)
            import_config_btn.grid(row=0, column=1, sticky="nsw", ipadx=14, ipady=8, padx=(10, 0), pady=(0, 0))

        return fila

    def __fillAssetFrame(self, asset_name, asset_config, asset_class, frame, fila):

        name_label = customtkinter.CTkLabel(frame, text=asset_name,
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        name_label.grid(row=fila, column=1, padx=(10, 20), pady=(10, 10), sticky="nsew")

        feature_label = customtkinter.CTkLabel(frame, text=asset_class,
                                               font=customtkinter.CTkFont(size=13, weight="normal"))
        feature_label.grid(row=fila, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        column = 3
        for feature in asset_config:

            if feature == "simulate" or feature == "active_hours" or \
                    feature == "calendar_range" or feature == "active_calendar":

                feature_label = customtkinter.CTkLabel(frame, text=asset_config[feature],
                                                        font=customtkinter.CTkFont(size=13, weight="normal"))
                feature_label.grid(row=fila, column=column, padx=(10, 10), pady=(10, 10), sticky="nsew")
                column += 1

    def __fillAssetTypeFrameColTitles(self, frame):

        t1 = customtkinter.CTkLabel(frame, text="class", font=customtkinter.CTkFont(size=14, weight="bold"))
        t2 = customtkinter.CTkLabel(frame, text="simulate", font=customtkinter.CTkFont(size=14, weight="bold"))
        t3 = customtkinter.CTkLabel(frame, text="active_hours", font=customtkinter.CTkFont(size=14, weight="bold"))
        t4 = customtkinter.CTkLabel(frame, text="calendar_range", font=customtkinter.CTkFont(size=14, weight="bold"))
        t5 = customtkinter.CTkLabel(frame, text="active_calendar", font=customtkinter.CTkFont(size=14, weight="bold"))

        t1.grid(row=0, column=2, padx=(10, 10), pady=(10, 20), sticky="nsew")
        t2.grid(row=0, column=3, padx=(10, 10), pady=(10, 20), sticky="nsew")
        t3.grid(row=0, column=4, padx=(10, 10), pady=(10, 20), sticky="nsew")
        t4.grid(row=0, column=5, padx=(10, 10), pady=(10, 20), sticky="nsew")
        t5.grid(row=0, column=6, padx=(10, 10), pady=(10, 20), sticky="nsew")


class SelectFrame(customtkinter.CTkFrame):

    def __init__(self, master, folder):
        super().__init__(master, corner_radius=14)

        self.folder = folder
        assets_dir = os.getcwd()
        assets_dir = os.path.join(assets_dir, "Asset_types")

        self.text = customtkinter.CTkLabel(self, text="Select the asset you want to add: ",
                                           font=customtkinter.CTkFont(size=16, weight="normal"))
        self.text.grid(row=0, column=0, padx=(50, 25), pady=(55, 10), sticky="nsew", columnspan=4, ipady=0)

        assets_list = os.listdir(os.path.join(assets_dir, folder))
        for element in assets_list:
            if element.__contains__(".toml"):
                assets_list.remove(element)

        self.optionemenu = customtkinter.CTkOptionMenu(self,
                                                       values=assets_list,
                                                       command=self.master.master.displayAssetConfig,
                                                       anchor=customtkinter.CENTER,
                                                       font=customtkinter.CTkFont(size=14, weight="normal"),
                                                       dropdown_font=customtkinter.CTkFont(size=14, weight="normal"),
                                                       dynamic_resizing=True,
                                                       width=200)
        self.optionemenu.grid(row=0, column=4, padx=0, pady=(55, 10), columnspan=1)
