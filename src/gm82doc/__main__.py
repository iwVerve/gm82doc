from markdown import markdownFromFile
from tempfile import TemporaryDirectory
from attrs import define, Factory
from typing import Union
from pathlib import Path


@define
class ScriptGroup:
    name: str
    children: list[Union["ScriptGroup", str]] = Factory(list)


@define
class Script:
    short_doc: str = ""
    long_doc: str = ""

    def __init__(self, name: str):
        self.short_doc = ""
        self.long_doc = ""


@define
class GM82Project:
    scripts: dict[str, Script]
    script_tree: ScriptGroup

    def __init__(self, project_path: str):
        self.scripts = {}
        self.script_tree = ScriptGroup("Scripts")
        self.open(project_path)

    def open(self, project_path_str: str):
        if not project_path_str.endswith("\\"):
            project_path_str += "\\"
        project_path = Path(project_path_str)

        script_folder = project_path.joinpath(r"scripts\\")
        script_tree_path = script_folder.joinpath(r"tree.yyd")

        script_tree = ScriptGroup("Scripts")
        current_path = []
        current_folder = script_tree
        current_depth = 0
        with script_tree_path.open() as script_tree_file:
            for line in script_tree_file.readlines():
                depth = len(line)
                line = line.lstrip("\t")
                depth -= len(line)

                while depth < current_depth:
                    current_folder = current_path.pop()
                    current_depth -= 1

                if line.startswith("+"):
                    line = line[1:-1]
                    new_folder = ScriptGroup(line)
                    current_folder.children.append(new_folder)
                    current_path.append(current_folder)
                    current_folder = new_folder
                    current_depth += 1
                elif line.startswith("|"):
                    line = line[1:-1]
                    new_script = Script(line)
                    self.scripts[line] = new_script
                    current_folder.children.append(line)


if __name__ == "__main__":
    project_path = (
        r"C:\Users\Ondra\Documents\GitHub\Verve-GM8.2-Engine\verve_gm82_engine.gm82"
    )
    project = GM82Project(project_path)
