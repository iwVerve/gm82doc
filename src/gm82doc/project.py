from attrs import define, Factory
from typing import Union
from pathlib import Path


@define
class ScriptFolder:
    name: str
    children: list[Union["ScriptFolder", str]] = Factory(list)


@define
class Script:
    signature: str = ""
    short_doc: str = ""
    long_doc: str = ""

    def __init__(self, name: str):
        self.short_doc = ""
        self.long_doc = ""


@define
class Project:
    path: str
    scripts: dict[str, Script]
    script_tree: ScriptFolder

    def __init__(self, project_path: str):
        self.path = project_path
        self.scripts = {}
        self.script_tree = ScriptFolder("Scripts")
        self.open()

    def open(self):
        self.read_script_tree()
        self.read_script_docs()

    def read_script_tree(self):
        current_path = []
        current_folder = self.script_tree
        current_depth = 0
        with self.get_script_tree().open() as script_tree_file:
            for line in script_tree_file.readlines():
                depth = len(line)
                line = line.lstrip("\t")
                depth -= len(line)

                while depth < current_depth:
                    current_folder = current_path.pop()
                    current_depth -= 1

                if line.startswith("+"):
                    line = line[1:-1]
                    new_folder = ScriptFolder(line)
                    current_folder.children.append(new_folder)
                    current_path.append(current_folder)
                    current_folder = new_folder
                    current_depth += 1
                elif line.startswith("|"):
                    line = line[1:-1]
                    new_script = Script(line)
                    self.scripts[line] = new_script
                    current_folder.children.append(line)

    def read_script_docs(self):
        for script_name, script in self.scripts.items():
            script_path = self.get_script_folder().joinpath(f"{script_name}.gml")
            with script_path.open() as script_file:
                state = 0
                can_read_signature = True
                can_read_short_doc = True
                can_read_long_doc = True
                for line in script_file.readlines():
                    line = line[:-1]

                    if state == 1:
                        if line.startswith("//"):
                            script.short_doc += " " + line[2:].strip()
                        else:
                            state = 0
                    elif state == 2:
                        if line == "*/":
                            state = 0
                            continue
                        else:
                            script.long_doc += line.strip() + "\n"

                    if state == 0:
                        if can_read_signature and line.startswith("///"):
                            script.signature = line[3 + len(script_name) :].strip()
                        elif can_read_short_doc and line.startswith("//"):
                            script.short_doc += line[2:].strip()
                            can_read_short_doc = False
                            state = 1
                        elif can_read_long_doc and line.startswith("/*doc"):
                            can_read_short_doc = False
                            can_read_long_doc = False
                            state = 2
                        elif line.strip() != "":
                            break

                    can_read_signature = False
                    if state == 0 and not can_read_short_doc and not can_read_long_doc:
                        break

    def get_script_folder(self) -> Path:
        return self.path.joinpath(r"scripts\\")

    def get_script_tree(self) -> Path:
        return self.get_script_folder().joinpath(r"tree.yyd")
