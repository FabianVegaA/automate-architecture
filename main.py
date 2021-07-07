import os
import pprint

from src.extractor import Extractor
from src.plotter import Plotter


def main():
    # Project path
    project = "."
    ignores = ["venv", "__pycache__", ".vscode"]

    # Get files and its importions
    path_imports = dict()

    extractor = Extractor(project, ignores)
    for path in extractor.extract_path_from():
        path_imports[path] = extractor.modules(extractor.extract_imports(path))

    # Make the architecture plot
    plotter = Plotter(name="_".join(project.split("/")), outformat="png")
    plotter.plot_code(project, path_imports)


if __name__ == "__main__":
    main()
