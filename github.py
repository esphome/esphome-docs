import csv
from itertools import zip_longest

from docutils import nodes, utils
from docutils.parsers.rst import directives, states
from docutils.parsers.rst.directives.tables import Table
from sphinx.util.nodes import make_refnode


def libpr_role(name, rawtext, text, lineno, inliner, options=None,
               content=None):
    ref = 'https://github.com/OttoWinter/esphomelib/pull/{}'.format(text)
    return [make_link_node(rawtext, 'lib#{}'.format(text), ref, options)], []


def yamlpr_role(name, rawtext, text, lineno, inliner, options=None,
                content=None):
    ref = 'https://github.com/OttoWinter/esphomeyaml/pull/{}'.format(text)
    return [make_link_node(rawtext, 'yaml#{}'.format(text), ref, options)], []


def docspr_role(name, rawtext, text, lineno, inliner, options=None,
                content=None):
    ref = 'https://github.com/OttoWinter/esphomedocs/pull/{}'.format(text)
    return [make_link_node(rawtext, 'docs#{}'.format(text), ref, options)], []


def ghuser_role(name, rawtext, text, lineno, inliner, options=None,
                content=None):
    ref = 'https://github.com/{}'.format(text)
    return [make_link_node(rawtext, '@{}'.format(text), ref, options)], []


def make_link_node(rawtext, text, ref, options=None):
    options = options or {}
    node = nodes.reference(rawtext,
                           utils.unescape(text),
                           refuri=ref,
                           **options)
    return node


# https://stackoverflow.com/a/3415150/8924614
def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


# Based on https://www.slideshare.net/doughellmann/better-documentation-through-automation-creating-docutils-sphinx-extensions
class ImageTableDirective(Table):

    option_spec = {}

    def run(self):
        env = self.state.document.settings.env

        items = []

        data = list(csv.reader(self.content))
        for row in data:
            if not row:
                continue
            name, page, image = row
            link = page.strip()
            if not link.startswith('http') and not link.startswith('/'):
                link = '/esphomeyaml/{}'.format(link)
            if '.html' not in link:
                link += '.html'
            items.append({
                'name': name.strip(),
                'link': link,
                'image': '/esphomeyaml/images/{}'.format(image.strip()),
            })

        col_widths = self.get_column_widths(3)
        title, messages = self.make_title()
        table = nodes.table()

        # Set up column specifications based on widths
        tgroup = nodes.tgroup(cols=3)
        table += tgroup
        tgroup.extend(
            nodes.colspec(colwidth=col_width)
            for col_width in col_widths
        )

        tbody = nodes.tbody()
        tgroup += tbody
        rows = []
        for value in grouper(3, items):
            trow = nodes.row()
            for cell in value:
                entry = nodes.entry()
                if cell is None:
                    entry += nodes.paragraph()
                    trow += entry
                    continue
                name = cell['name']
                link = cell['link']
                image = cell['image']
                reference_node = nodes.reference(refuri=link)
                img = nodes.image(uri=directives.uri(image), alt=name)
                img['classes'].append('component-image')
                reference_node += img
                para = nodes.paragraph()
                para += reference_node
                entry += para
                trow += entry
            rows.append(trow)

            trow = nodes.row()
            for cell in value:
                entry = nodes.entry()
                if cell is None:
                    entry += nodes.paragraph()
                    trow += entry
                    continue
                name = cell['name']
                link = cell['link']
                ref = nodes.reference(name, name, refuri=link)
                para = nodes.paragraph()
                para += ref
                entry += para
                trow += entry
            rows.append(trow)
        tbody.extend(rows)

        table['classes'] += []
        self.add_name(table)
        if title:
            table.insert(0, title)

        return [table] + messages


class PinTableDirective(Table):
    option_spec = {}

    def run(self):
        env = self.state.document.settings.env

        items = []

        data = list(csv.reader(self.content))
        for row in data:
            if not row:
                continue
            if len(row) == 3:
                items.append((row[0], row[1], True))
            else:
                items.append((row[0], row[1], False))

        col_widths = self.get_column_widths(2)
        title, messages = self.make_title()
        table = nodes.table()

        # Set up column specifications based on widths
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup.extend(
            nodes.colspec(colwidth=col_width)
            for col_width in col_widths
        )

        thead = nodes.thead()
        tgroup += thead
        trow = nodes.row()
        thead += trow
        trow.extend(
            nodes.entry(h, nodes.paragraph(text=h))
            for h in ('Pin', 'Function')
        )

        tbody = nodes.tbody()
        tgroup += tbody
        for name, func, important in items:
            trow = nodes.row()
            entry = nodes.entry()
            para = nodes.paragraph()
            para += nodes.literal(text=name)
            entry += para
            trow += entry

            entry = nodes.entry()
            if important:
                para = nodes.paragraph()
                para += nodes.strong(text=func)
            else:
                para = nodes.paragraph(text=func)
            entry += para
            trow += entry
            tbody += trow

        table['classes'] += ['no-center']
        self.add_name(table)
        if title:
            table.insert(0, title)

        return [table] + messages


def setup(app):
    app.add_role('libpr', libpr_role)
    app.add_role('yamlpr', yamlpr_role)
    app.add_role('docspr', docspr_role)
    app.add_role('ghuser', ghuser_role)
    app.add_directive('imgtable', ImageTableDirective)
    app.add_directive('pintable', PinTableDirective)
