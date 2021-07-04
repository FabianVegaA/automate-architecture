from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from re import search


def plot_code(project, import_files):
    with Diagram(project, direction="TB"):
        for path, imports in import_files.items():

            
            filtered_imports = [
                tuple(filter(lambda i: i is not None, import_)) for import_ in imports
            ]
            if filtered_imports:
                node = folder(path)
                for i in filtered_imports:
                    Python(str(i[0])) >> node


def folder(path: str):
    d = path.split("/")
    if len(d) == 1:
        return Python(d[0])
    else:
        with Cluster(d[0]):
            return folder("".join(d[1:]))
