from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from re import search
import pprint


class Plotter:
    def __init__(self, name="Diagram", direction="TB"):
        self.imports = dict()
        self.name = name
        self.direction = direction
        self.filename = f"out/diagram_{self.name}"

    def plot_code(self, project, import_files):
        with Diagram(
            f"Diagram {project}",
            direction=self.direction,
            filename=self.filename,
        ):
            with Cluster(project):
                for path, imports in import_files.items():

                    filtered_imports = [
                        tuple(filter(lambda i: i is not None, import_))
                        for import_ in imports
                    ]
                    self._make_edges(path, filtered_imports)

    def _make_edges(self, path, filtered_imports):

        if filtered_imports:
            node = self._folder(path)

            for importations in filtered_imports:
                for sub_import_ in importations:
                    if sub_import_ in self.imports.keys():
                        self.imports.get(sub_import_) >> node
                    else:
                        self.imports[sub_import_] = Python(sub_import_)
                        self.imports.get(sub_import_) >> node

    def _folder(self, path: str):
        d = path.split("/")
        if len(d) == 1:
            return Python(d[0])
        else:
            with Cluster(d[0]):
                return self._folder("/".join(d[1:]))
