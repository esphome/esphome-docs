# generates a JSONSchema for completion and help

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend


def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(
        components=components).get_default_values()
    document = docutils.utils.new_document('<rst-doc>', settings=settings)
    parser.parse(text, document)
    return document


class MyVisitor(docutils.nodes.NodeVisitor):
    def __init__(self, doc):
        super().__init__(doc)
        self.indent = ''

    def visit_reference(self, node: docutils.nodes.reference) -> None:
        """Called for "reference" nodes."""
        # print(node)

    def visit_title(self, node: docutils.nodes.reference) -> None:
        print(str(type(node)) + str(node)[0:90])

    def visit_paragraph(self, node: docutils.nodes.reference) -> None:
        """Called for "reference" nodes."""
        # print(node)

    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        """Called for all other node types."""
        #+ ' ' + str(node)
        print('  ' + str(type(node)) + str(node)[0:90])
        pass


file = open('components/esphome.rst', 'r')

doc = parse_rst(file.read())
visitor = MyVisitor(doc)
doc.walk(visitor)
