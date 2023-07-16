from typing import Any
from markdown import Markdown, Extension
from markdown.postprocessors import Postprocessor


class MyPostprocessor(Postprocessor):
    def run(self, text) -> Any:
        return text.replace("<code>", "<tt>").replace("</code>", "</tt>")


class MyExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.postprocessors.register(MyPostprocessor(), "", 100)
