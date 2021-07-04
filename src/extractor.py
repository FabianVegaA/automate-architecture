import re
import os


_IMPORT_PATTERN = re.compile(
    r"^import ([a-zA-Z1-9\.]+)|^from ([a-zA-Z1-9\.]+) import ([\w, ]+)",
    flags=re.MULTILINE,
)


def extract_imports(path: str):
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


def extract_path_from(path: str):
    for root, dirs, files in os.walk(path):
        for f in files:
            if _is_python_file(f):
                yield f"{root}/{f}"


def _is_python_file(file_):
    return bool(re.search(r".\.py$", file_))
