# Utilities document for common functions, classes and values

import importlib


def createClass(path, asset_type):

    path_module = path.replace(".", "")
    path_module = path_module.replace("/", ".")
    path_module = path_module.replace("\\", ".")
    # Canvis a la string del path perquè els mòduls s'importen amb format Abstraction.Asset_types. ...

    module = importlib.import_module(path_module + "." + asset_type)
    classe = getattr(module, asset_type)  # Obtenim la classe que hem de crear ara (Electrolyzer, EVCharger...)

    return classe


def isNumber(value):

    if value.isnumeric():
        return True
    else:

        try:
            float(value)
            return True
        except ValueError:
            return False


def toNumber(value):

    if value.__contains__("."):
        return float(value)
    else:
        return int(value)
