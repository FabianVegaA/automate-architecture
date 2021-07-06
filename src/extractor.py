import re
import os


_IMPORT_PATTERN = re.compile(
    r"^import ([a-zA-Z1-9\.]+)|^from ([a-zA-Z1-9\.]+) import ([\w, ]+)",
    flags=re.MULTILINE,
)


class Extractor:
    def __init__(self, path: str, ignores: list = None):
        self.ignores = ignores
        self.path = path

    def extract_imports(self, path):
        with open(path, mode="r", encoding="UTF-8") as file:
            content = "".join(file.readlines())
            for match in re.finditer(_IMPORT_PATTERN, content):
                yield (
                    path,
                    tuple(
                        sum(
                            map(
                                lambda i: i.split(", ") if i is not None else [i],
                                match.groups(),
                            ),
                            [],
                        )
                    ),
                )

    def modules(self, generator):
        return [
            ".".join(filter(lambda i: i is not None, t))
            for t in sum(
                [
                    [
                        (imports[0], imports[1], imports[i])
                        for i in range(2, len(imports))
                    ]
                    if len(imports) > 3
                    else [imports]
                    for _, imports in generator
                ],
                [],
            )
        ]

    def extract_path_from(self):
        for root, dirs, files in os.walk(self.path):
            if not self._has_match(root):
                for file in files:
                    if self._is_python_file(file):
                        yield f"{root}/{file}"
            else:
                print(f"Ignored {root}")

    def _has_match(self, root):
        if self.ignores:
            for ignore in self.ignores:
                if ignore in root:
                    return True
        return False

    def _is_python_file(self, file):
        return bool(re.search(r".\.py$", file))
