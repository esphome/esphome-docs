# Based on https://github.com/rmk135/sphinxcontrib-disqus
from docutils import nodes
from docutils.parsers.rst import Directive


class DisqusNode(nodes.General, nodes.Element):
    def __init__(self, disqus_identifier):
        super(DisqusNode, self).__init__()
        self.disqus_identifier = disqus_identifier


def disqus_visit(self, node):
    html_attrs = {
        'ids': ['disqus_thread'],
        'data-disqus-identifier': node.disqus_identifier,
    }
    self.body.append(self.starttag(node, 'div', '', **html_attrs))


def disqus_depart(self, _):
    self.body.append('</div>')


class DisqusDirective(Directive):
    option_spec = dict(identifier=str)

    def get_identifier(self):
        if 'identifier' in self.options:
            return self.options['identifier']

        env = self.state.document.settings.env
        return env.docname.replace('/', '-')

    def run(self):
        disqus_identifier = self.get_identifier()
        return [DisqusNode(disqus_identifier)]


def event_html_page_context(app, pagename, templatename, context, doctree):
    if not doctree or 'script_files' not in context:
        return
    if any(hasattr(n, 'disqus_identifier') for n in doctree.traverse()):
        context['script_files'] = context['script_files'][:] + ['_static/disqus.js']


def setup(app):
    app.add_directive('disqus', DisqusDirective)
    app.add_node(DisqusNode, html=(disqus_visit, disqus_depart))
    app.connect('html-page-context', event_html_page_context)
    return {'version': '1.0'}
