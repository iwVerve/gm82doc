from .project import Project
from .html import generate_output
from .config import HHC_PATH
from subprocess import run
from tempfile import TemporaryDirectory
from pathlib import Path
from shutil import copyfile
from sys import argv


if __name__ == "__main__":
    if len(argv) >= 2:
        project_path = Path(argv[1])
        if not project_path.is_dir():
            project_path = project_path.parent
        project = Project(project_path)
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            generate_output(project, temp_dir)
            run([HHC_PATH, temp_path.joinpath("help.chm")])
            copyfile(temp_path.joinpath("help.chm"), project_path.joinpath("help.chm"))
    else:
        print("""Usage: py -m gm82doc <project folder>""")
