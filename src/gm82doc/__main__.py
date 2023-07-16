from .project import Project
from .html import generate_output

if __name__ == "__main__":
    project_path = (
        r"C:\Users\Ondra\Documents\GitHub\Verve-GM8.2-Engine\verve_gm82_engine.gm82"
    )
    output_path = r"C:\Users\Ondra\Desktop\Temp\out"
    project = Project(project_path)
    generate_output(project, output_path)
