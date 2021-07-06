from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from re import search
import pprint


class Plotter:

    _default_graph_attrs = {
        "pad": "2.0",
        "splines": "ortho",
        "nodesep": "0.60",
        "ranksep": "0.75",
        "fontname": "Sans-Serif",
        "fontsize": "13",
        "fontcolor": "#2D3436",
    }
    _default_node_attrs = {
        "shape": "box",
        "style": "rounded",
        "fixedsize": "true",
        "width": "1.4",
        "height": "1.4",
        "labelloc": "b",
        "imagescale": "true",
        "fontname": "Sans-Serif",
        "fontsize": "13",
        "fontcolor": "#2D3436",
    }
    _default_edge_attrs = {
        "color": "#7B8894",
    }

    def __init__(
        self,
        name="Diagram",
        direction="TB",
        curvestyle="ortho",
        outformat="png",
        graph_attr=None,
        node_attr=None,
        edge_attr=None,
    ):
        self.imports = dict()
        self.name = name
        self.direction = direction
        self.filename = f"out/diagram_{self.name}"
        self.curvestyle = curvestyle
        self.outformat = outformat
        self.graph_attr = graph_attr if graph_attr else self._default_graph_attrs
        self.node_attr = node_attr if node_attr else self._default_node_attrs
        self.edge_attr = edge_attr if node_attr else self._default_edge_attrs

    def plot_code(self, project, import_files):
        with Diagram(
            name=f"Diagram {project}",
            direction=self.direction,
            filename=self.filename,
            curvestyle=self.curvestyle,
            outformat=self.outformat,
            graph_attr=self.graph_attr,
            node_attr=self.node_attr,
            edge_attr=self.edge_attr,
        ):
            with Cluster("project", direction="LR"):
                for path, imports in import_files.items():

                    self._make_edges(path, imports)

    def _make_edges(self, path, imports):
        node = self._folder(path)

        for importation in imports:
            if len(importation) > 15:
                importation = f"{importation[0:15]}\n{importation[15:]}"
            if importation in self.imports.keys():
                self.imports.get(importation) >> node
            else:
                self.imports[importation] = Storage(importation)
                self.imports.get(importation) >> node

    def _folder(self, path: str):
        d = path.split("/")
        if len(d) == 1:
            return Python(d[0])
        else:
            with Cluster(d[0], direction="LR"):
                return self._folder("/".join(d[1:]))
