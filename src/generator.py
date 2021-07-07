import yaml
from yaml.loader import SafeLoader

import importlib


def get_importation(section: str, subsection: str):
    with open("classes_diagrams.yaml", "r") as file:
        imports = yaml.load(file, Loader=SafeLoader)

    importation = imports.get(section, dict()).get(subsection, None)

    mod = importlib.import_module(importation.split(" ")[1])
    return eval("mod.{}".format(importation.split(" ")[-1]))


mod = get_importation("aws", "adconnector")

print(mod.__name__, dir(mod))
