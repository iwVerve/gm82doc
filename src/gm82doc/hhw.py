from typing import TextIO
from .project import Project, ScriptFolder


def generate_hhp_file_path(path: str, files: list):
    with open(path, "w") as file:
        generate_hhp_file(file, path.parent, files)


def generate_hhp_file(output: TextIO, root: str, files: list):
    output.write(
        "\n".join(
            [
                "[OPTIONS]",
                "Contents file=help.hhc",
                "Index file=help.hhk",
                "",
                "[FILES]",
            ]
        )
    )
    output.write("\n")
    for file in files:
        output.write(f"{file.relative_to(root)}\n")


def generate_hhc_file_path(path: str, project: Project):
    with open(path, "w") as file:
        generate_hhc_file(file, project)


def generate_hhc_item(output: TextIO, name: str, path: str):
    output.write(
        f"""\t<LI> <OBJECT type="text/sitemap">
\t\t<param name="Name" value="{name}">
\t\t<param name="Local" value="{path}">
\t\t</OBJECT>"""
    )


def generate_hhc_file(output: TextIO, project: Project):
    output.write(
        """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<HTML>
<HEAD>
<meta name="GENERATOR" content="Microsoft&reg; HTML Help Workshop 4.1">
<!-- Sitemap 1.0 -->
</HEAD><BODY>
<OBJECT type="text/site properties">
	<param name="Window Styles" value="0x800025">
</OBJECT>
<UL>\n"""
    )
    generate_hhc_item(output, "Documentation", r"files\index.html")
    output.write(
        """</UL>
</BODY>
</HTML>"""
    )


def generate_hhk_folder(output: TextIO, folder: ScriptFolder, project: Project):
    for child in folder.children:
        if isinstance(child, str):
            script = project.scripts[child]
            if script.long_doc != "":
                generate_hhk_item(output, child, child, rf"files\{child}.html")
            else:
                generate_hhk_item(output, child, "index", "index.html")
        else:
            generate_hhk_folder(output, child, project)


def generate_hhk_item(
    output: TextIO, name: str, destination_name: str, destination: str
):
    output.write(
        f"""\t<LI> <OBJECT type="text/sitemap">
\t\t<param name="Name" value="{name}">
\t\t<param name="Name" value="{destination_name}">
\t\t<param name="Local" value="{destination}">
\t\t</OBJECT>\n"""
    )


def generate_hhk_file_path(path: str, project: Project):
    with open(path, "w") as file:
        generate_hhk_file(file, project)


def generate_hhk_file(output: TextIO, project: Project):
    output.write(
        """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<HTML>
<HEAD>
<meta name="GENERATOR" content="Microsoft&reg; HTML Help Workshop 4.1">
<!-- Sitemap 1.0 -->
</HEAD><BODY>
<UL>
"""
    )
    generate_hhk_item(output, "index", "index", "index.html")
    generate_hhk_folder(output, project.script_tree, project)
    output.write(
        """</UL>
</BODY>
</HTML>
"""
    )
