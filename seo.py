import re

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.writers._html_base import HTMLTranslator


class SEONode(nodes.General, nodes.Element):
    def __init__(self, title=None, description=None, image=None,
                 author=None, author_twitter=None, keywords=None):
        super(SEONode, self).__init__()
        self.title = title
        self.description = description
        self.image = image
        self.author = author
        self.author_twitter = author_twitter
        self.keywords = keywords


def seo_visit(self: HTMLTranslator, node: SEONode):
    def encode_text(text):
        special_characters = {ord('&'): '&amp;',
                              ord('<'): '&lt;',
                              ord('"'): '&quot;',
                              ord('>'): '&gt;'}
        return text.translate(special_characters)

    def create_content_meta(name, content):
        if content is None:
            return
        self.meta.append('<meta name="{}" content="{}">\n'.format(name, encode_text(content)))

    def create_itemprop_meta(name, content):
        if content is None:
            return
        self.meta.append('<meta itemprop="{}" content="{}">\n'.format(name, encode_text(content)))

    def create_property_meta(name, content):
        if content is None:
            return
        self.meta.append('<meta property="{}" content="{}"/>\n'.format(name, encode_text(content)))

    # Base
    create_content_meta("description", node.description)
    create_content_meta("keywords", node.keywords)

    # Schema.org
    create_itemprop_meta("name", node.title)
    create_itemprop_meta("description", node.description)
    create_itemprop_meta("image", node.image)

    # Twitter
    create_content_meta("twitter:title", node.title)
    create_content_meta("twitter:image:src", node.image)
    create_content_meta("twitter:card", "summary_large_image")
    create_content_meta("twitter:site", "@OttoWinter_")
    create_content_meta("twitter:creator", node.author_twitter)
    create_content_meta("twitter:description", node.description)

    # Open Graph
    create_property_meta("og:title", node.title)
    create_property_meta("og:image", node.image)
    create_property_meta("og:type", "article" if node.author is not None else "website")
    create_property_meta("og:site_name", "esphomelib")
    create_property_meta("og:description", node.description)

    # Misc
    create_content_meta("HandheldFriendly", "True")
    create_content_meta("MobileOptimized", "320")
    create_content_meta("theme-color", "#DFDFDF")


def seo_depart(self, _):
    pass


class SEODirective(Directive):
    option_spec = {
        'title': directives.unchanged,
        'description': directives.unchanged,
        'image': directives.path,
        'author': directives.unchanged,
        'author_twitter': directives.unchanged,
        'keywords': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        title_match = re.match(r'.+<title>(.+)</title>.+', str(self.state.document))
        if title_match is not None and 'title' not in self.options:
            self.options['title'] = title_match.group(1)

        image = self.options.get('image')
        if image is not None:
            if not image.startswith('/'):
                image = '/_images/' + image
            self.options['image'] = env.config.html_baseurl + image
        description = self.options.get('description')
        if description is not None and len(description) >= 200:
            self.options['description'] = description[:200].rsplit(' ', 1)[0] + '...'

        return [SEONode(**self.options)]


def setup(app):
    app.add_directive('seo', SEODirective)
    app.add_node(SEONode, html=(seo_visit, seo_depart))
    return {'version': '1.0'}
