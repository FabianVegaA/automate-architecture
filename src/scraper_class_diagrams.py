import requests
from bs4 import BeautifulSoup
import pprint
import yaml

_NODES = [
    "onprem",
    "aws",
    "azure",
    "gcp",
    "k8s",
    "alibabacloud",
    "oci",
    "openstack",
    "firebase",
    "outscale",
    "elastic",
    "generic",
    "programming",
    "saas",
]

_URL = "https://diagrams.mingrammer.com/docs/nodes/{}"

_DIAGRAM_PAGES = {node: requests.get(_URL.format(node)) for node in _NODES}


def transform_in_import(class_import):
    class_import_list = class_import.split(".")
    return "from {} import {}".format(
        ".".join(class_import_list[:-1]), class_import_list[-1]
    )


def save_importations(data):
    with open("classes_diagrams.yaml", "+w") as file:
        yaml.dump(data, file)


def get_importations():
    for node, label in (
        (node, BeautifulSoup(page.text, "html").find("article").find_all("strong"))
        for node, page in _DIAGRAM_PAGES.items()
    ):
        importations = dict()

        for sec in label:
            if "diagrams." in sec.get_text():
                text = transform_in_import(sec.get_text())

                importations[text.split(" ")[-1].lower()] = text

        yield (node, importations)


save_importations({n: t for n, t in get_importations()})
