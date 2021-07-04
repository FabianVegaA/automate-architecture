import os

from src.extractor import extract_imports, extract_path_from
from src.plotter import plot_code


def main():
    
    project = "src"
    path_imports = dict()
    for path in extract_path_from(project):
        path_imports[path] = [imports for _, imports in extract_imports(path)]

    print(path_imports)
    plot_code(f"directory {project}", path_imports)


if __name__ == "__main__":
    main()
