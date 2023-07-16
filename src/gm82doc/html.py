from .project import Project, ScriptFolder, Script
from yattag import SimpleDoc, indent
from pathlib import Path
from pkgutil import get_data
from markdown import markdown


def generate_head(doc: SimpleDoc, title: str):
    _, tag, text = doc.tagtext()

    with tag("head"):
        with tag("title"):
            text(title)
        doc.stag("link", href="style.css", rel="stylesheet", type="text/css")


def generate_keywords(doc: SimpleDoc, keywords: list):
    _, tag, text = doc.tagtext()

    doc.asis("<!-- KEYWORDS\n")
    for keyword in keywords:
        doc.text(f"{keyword}\n")
    doc.asis("-->")


def generate_script_folder(doc: SimpleDoc, project: Project, folder: ScriptFolder):
    _, tag, text = doc.tagtext()
    with tag("ul"):
        with tag("li"):
            text(folder.name)
        for child in folder.children:
            if isinstance(child, str):
                script = project.scripts[child]
                with tag("li"):
                    with tag("tt"):
                        if script.long_doc == "":
                            text(child)
                        else:
                            with tag("a", href=f"{child}.html"):
                                text(child)
                    doc.text(f"\n{script.short_doc}")
                    doc.asis("<br>\n")
            else:
                generate_script_folder(doc, project, child)


def generate_index_body(doc: SimpleDoc, project: Project):
    _, tag, text = doc.tagtext()

    with tag("body", background="images/back.gif"):
        doc.asis("<!--START-->")
        with tag("h3"):
            text("Project index")
        doc.asis("<p>")
        with tag("blockquote"):
            generate_script_folder(doc, project, project.script_tree)
        doc.asis("<!--END-->")


def generate_index(project: Project) -> str:
    doc, tag, text = SimpleDoc(stag_end=">").tagtext()

    doc.asis('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">')
    with tag("html"):
        generate_head(doc, "index")
        generate_index_body(doc, project)
    generate_keywords(doc, ["index"])

    return indent(doc.getvalue(), indentation="")


def generate_script_page(script_name: str, script: Script) -> str:
    doc, tag, text = SimpleDoc(stag_end=">").tagtext()

    doc.asis('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">')
    with tag("html"):
        generate_head(doc, script_name)
        with tag("body", background="images/back.gif"):
            doc.asis("<!--START-->")
            with tag("a", href="index.html"):
                text("Back to index")
            with tag("h3"):
                text(script_name)
            doc.asis("<p>")
            with tag("blockquote"):
                text(f"{script_name}{script.signature}")
                with tag("p"):
                    text(script.short_doc)
                doc.asis(markdown(script.long_doc))
            doc.asis("<!--END-->")
    generate_keywords(doc, [script_name])

    return indent(doc.getvalue(), indentation="")


def generate_output(project: Project, path: str):
    output_dir = Path(path)
    index_path = output_dir.joinpath("index.html")
    stylesheet_path = output_dir.joinpath("style.css")
    images_dir = output_dir.joinpath("images/")
    back_path = images_dir.joinpath("back.gif")

    output_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    with open(index_path, "w") as index_file:
        index_file.write(generate_index(project))
    with open(stylesheet_path, "wb") as stylesheet_file:
        style_bytes = get_data(__name__, r"data\style.css")
        stylesheet_file.write(style_bytes)
    with open(back_path, "wb") as back_file:
        back_bytes = get_data(__name__, r"data\back.gif")
        back_file.write(back_bytes)

    for script_name, script in project.scripts.items():
        if script.long_doc != "":
            script_path = output_dir.joinpath(f"{script_name}.html")
            with open(script_path, "w") as script_file:
                script_file.write(generate_script_page(script_name, script))
