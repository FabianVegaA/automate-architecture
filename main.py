import os
import pprint

from src.extractor import extract_imports, extract_path_from
from src.plotter import Plotter


def main():
    # Project path
    project = "src"

    # Get files and its importions
    path_imports = dict()
    for path in extract_path_from(project):
        path_imports[path] = [imports for _, imports in extract_imports(path)]

    # Make the architecture plot
    plotter = Plotter(name="_".join(project.split("/")))
    plotter.plot_code(project, path_imports)


if __name__ == "__main__":
    main()
