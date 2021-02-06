import re
import docutils
from markdown import MDWriter
import os
import xml.etree.ElementTree as ET
import json
from docutils import nodes
from docutils.core import publish_doctree, publish_file, publish_from_doctree


def setup(app):
    """Setup connects events to the sitemap builder"""
    app.connect('html-page-context', add_html_link)
    app.connect('doctree-resolved', doctree_resolved)
    app.connect('build-finished', test_jschema)
    f = open('../esphome_devices/schema.json', 'r', encoding="utf-8-sig")
    str = f.read()
    app.jschema = json.loads(str)

    return {"version": "1.0.0",
            "parallel_read_safe": True,
            "parallel_write_safe": True}


def doctree_resolved(app, doctree, docname):
    try:
        if docname.startswith('components/'):
            component = docname[11:]
            jc = app.jschema["definitions"].get("schema_" + component)
            if jc:
                handle_component(app, jc, doctree, docname)
        print()
        print('doctree resolverd: ' + str(docname))
    except Exception as e:
        e = e


def handle_component(app, jschema, doctree, docname):
    print('handling ' + docname)
    props = jschema["properties"]
    if props:
        for section in doctree.traverse(nodes.section):
            title = section.next_node(nodes.Titular)
            if title and title.astext() == "Configuration variables:":
                # html = publish_from_doctree(title, writer_name='html').decode()
                # print(html)
                for config in title.traverse(nodes.list_item, siblings=True):
                    key = config.traverse(nodes.Text)[0].astext()
                    if key in props:
                        update_prop(app, docname, config, props)


def update_prop(app, docname, node, jschema):
    # There might be a better way to do this

    raw = node.rawsource  # this has the full raw rst code for this property
    sep_idx = raw.index(': ')
    # todo error
    name_type = raw[:sep_idx]

    # Example properties formats are:
    # **name** (**Required**, string): Long Description...
    # **name** (*Optional*, string): Long Description... Defaults to ``value``.
    # **name** (*Optional*): Long Description... Defaults to ``value``.

    ntr = re.search(
        '(\*\*(\w*)\*\*)\s(\(((\*\*Required\*\*)|(\*Optional\*))(, ([\w\s]+))*)\)', name_type, re.IGNORECASE)

    if ntr:
        prop_name = ntr.group(2)
        req = ntr.group(4)
        param_type = ntr.group(8)

    # todo check props valid, and prop in jschema
    jprop = jschema[str(prop_name)]

    description = raw[sep_idx + 2:]
    # remove whitespace
    description = ' '.join([x.strip() for x in description.split('\n')])
    # convert full urls
    description = re.sub(
        pattern='`([\w\s]+)\s{1}<(((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*)>`__',
        repl='[\\1](\\2)',
        string=description
    )
    # convert doc refs
    description = re.sub(
        pattern=':doc:`([\w\s]+)(<([/]\w*)*>)?`',
        string=description,
        repl=lambda r: ':doc:(' + str(r) + ')'
    )
    # local-refs
    local_url = app.config.html_baseurl + '/' + docname + '.html#'

    description = re.sub(
        pattern=':ref:`([-\w\s]+)`',
        string=description,
        repl=lambda r: local_url + str(r.group(1)).replace('_', '-')
    )
    link_title = node.traverse()[8].astext()
    x = type(node.traverse(nodes.reference)[0])
    jprop["markdownDescription"] = description.strip()


def add_html_link(app, pagename, templatename, context, doctree):
    print('add_html_link: ' + str(pagename))


def test_jschema(app, exception):

    f = open('../esphome_devices/schema.json', 'w', encoding="utf-8-sig")

    f.write(json.dumps(app.jschema))
