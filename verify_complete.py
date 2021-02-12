import re
import docutils
from markdown import MDWriter
import os
import xml.etree.ElementTree as ET
import json
from docutils import nodes
from docutils.core import publish_doctree, publish_file, publish_from_doctree

SCHEMA_PATH = '../esphome_devices/schema.json'
# SCHEMA_PATH = '../esphome-vscode/server/src/schema.json'


def setup(app):
    """Setup connects events to the sitemap builder"""
    app.connect('html-page-context', add_html_link)
    app.connect('doctree-resolved', doctree_resolved)
    app.connect('build-finished', test_jschema)
    f = open(SCHEMA_PATH, 'r', encoding="utf-8-sig")
    str = f.read()
    app.jschema = json.loads(str)

    return {"version": "1.0.0",
            "parallel_read_safe": True,
            "parallel_write_safe": True}


def find_platform(jschema, component, platform):
    ar = jschema["properties"][component]["items"]['allOf']
    for p in ar:
        if p["if"]["properties"]["platform"]["const"] == platform:
            return p
    raise ValueError("Cannot find {} platform {}".format(component, platform))


def doctree_resolved(app, doctree, docname):
    try:
        handle_component(app, doctree, docname)
        # path = docname.split('/')
        # if path[0] == 'components':
        #     if len(path) == 2:  # root component, e.g. dfplayer, logger
        #         component = docname[11:]
        #         jc = app.jschema["definitions"].get("schema_" + component)
        #         if jc:
        #             # multi configuration schemas are in definitions, e.g.
        #             # i2c, dallas
        #             handle_component(app, jc, doctree, docname)
        #         else:
        #             jc = app.jschema["properties"].get(component)
        #             if jc:
        #                 # single config like logger, wifi
        #                 handle_component(app, jc, doctree, docname)
        #     else:  # sub component, e.g. output/esp8266_pwm

        #         # components here might have a core / hub, eg. dallas, ads1115
        #         # and then they can be a binary_sensor, sensor, etc.

        #         component = path[1]
        #         platform = path[2]
        #         if platform == 'index':
        #             # Handle subcomponent index, e.g. output, sensor
        #             return

        #         jc = app.jschema["properties"].get(platform)

        #         jp = find_platform(app.jschema, component, platform)
        #         if jc is not None:
        #             handle_component_with_hub(
        #                 app, jp["then"], doctree, docname, jc)
        #         else:
        #             handle_component(app, jp["then"], doctree, docname)

        print('doctree resolverd: ' + str(docname))
    except Exception as e:
        e = e
        print(e)


def get_ref(jschema, node):
    ref = node.get('$ref')
    if ref and ref.startswith('#/definitions/'):
        return jschema["definitions"][ref[14:]]


def find_props(node, app):
    # find properties
    if "then" in node:
        node = node["then"]
    props = node.get("properties")
    ref = None
    if not props:
        arr = node.get('anyOf', node.get('allOf'))
        for x in arr:
            props = x.get('properties')
            if not ref:
                ref = get_ref(app.jschema, x)
            if props:
                break
    if not props and ref:
        return find_props(ref, app)

    return props


def handle_component(app, doctree, docname):

    path = docname.split('/')
    json_component = None
    json_platform = None
    if path[0] == 'components':
        if len(path) == 2:  # root component, e.g. dfplayer, logger
            component = docname[11:]
            json_component = app.jschema["definitions"].get(
                "schema_" + component)
            if not json_component:
                #     # multi configuration schemas are in definitions, e.g.
                #     # i2c, dallas
                #     handle_component(app, jc, doctree, docname)
                # else:
                json_component = app.jschema["properties"].get(component)
            #     if jc:
            #         # single config like logger, wifi
            #         handle_component(app, jc, doctree, docname)
        else:  # sub component, e.g. output/esp8266_pwm

            # components here might have a core / hub, eg. dallas, ads1115
            # and then they can be a binary_sensor, sensor, etc.

            component = path[1]
            platform = path[2]
            if platform == 'index':
                # Handle subcomponent index, e.g. output, sensor
                return

            json_component = app.jschema["properties"].get(platform)

            json_platform = find_platform(app.jschema, component, platform)
            # if json_component is not None:
            #     handle_component_with_hub(
            #         app, json_platform["then"], doctree, docname, json_component)
            # else:
            #     handle_component(app, json_platform["then"], doctree, docname)

    # ESPHome page docs follows strict formating guidelines which allows
    # for docs to be parsed directly into yaml schema

    # Document first paragraph is description of this thing
    description = getMarkdown(app, docname, doctree,
                              doctree.traverse(nodes.paragraph)[0])
    if json_component:
        json_component["markdownDescription"] = description
    else:
        json_platform["markdownDescription"] = description

    hub_found = False
    component_found = False
    props = None
    for section in doctree.traverse(nodes.section):
        # First title is the component title, e.g.
        # components/ads1115.rst ADS115 Sensor
        # Second title must be 'Component/Hub' for components with both
        # json_component and json_schema, these are components with hub
        title = section.next_node(nodes.Titular)
        if not title:
            continue
        title_text = title.astext()
        if title_text == 'Component/Hub':
            hub_found = True
            try:
                props = find_props(json_component, app)
            except:
                raise ValueError('Cannot find hub props for ' + docname)
        if title_text == "Configuration variables:":
            if not props:
                raise ValueError(
                    'Found a Configuration variables title but dont kow to whic props to fill. ' + docname)
            # This is a section of configuration, update props with this section
            for config in title.traverse(nodes.list_item, siblings=True):
                key = config.traverse(nodes.Text)[0].astext()
                if key in props:
                    update_prop(app, doctree, docname, config, props)
        if title_text == 'Sensor':
            # Now fill props for the platform element
            try:
                props = find_props(json_platform, app)
            except:
                raise ValueError('Cannot find platform props for ' + docname)
        if title_text.endswith('Component'):
            component_found = True
            try:
                props = find_props(json_component, app)
            except:
                raise ValueError('Cannot find component props for ' + docname)


def handle_component_old(app, jschema, doctree, docname):
    print('handling ' + docname)

    jschema["markdownDescription"] = getMarkdown(
        app, docname, doctree, doctree.traverse(nodes.paragraph)[0])

    try:
        props = find_props(jschema)
    except:
        raise ValueError('Cannot find props for ' + docname)

    for section in doctree.traverse(nodes.section):
        title = section.next_node(nodes.Titular)
        if title and title.astext() == "Configuration variables:":
            # html = publish_from_doctree(title, writer_name='html').decode()
            # print(html)
            for config in title.traverse(nodes.list_item, siblings=True):
                key = config.traverse(nodes.Text)[0].astext()
                if key in props:
                    update_prop(app, doctree, docname, config, props)


def getMarkdown(app, docname, doctree, node):
    from urllib import parse
    from markdown import Translator
    t = Translator(parse.urljoin(
        app.config.html_baseurl, docname + '.html'), doctree)
    node.walkabout(t)
    return t.output


def update_prop(app, doctree, docname, node, jschema):
    try:
        markdown = getMarkdown(app, docname, doctree, node)

        raw = node.rawsource  # this has the full raw rst code for this property

        sep_idx = raw.index(': ')
        # todo error
        name_type = raw[:sep_idx]

        # Example properties formats are:
        # **name** (**Required**, string): Long Description...
        # **name** (*Optional*, string): Long Description... Defaults to ``value``.
        # **name** (*Optional*): Long Description... Defaults to ``value``.

        if 'ads111' in docname:
            docname = docname

        ntr = re.search(
            '\* \*\*(\w*)\*\*\s(\(((\*\*Required\*\*)|(\*Optional\*))(,\s(.*))*)\):\s', markdown, re.IGNORECASE)

        if ntr:
            prop_name = ntr.group(1)
            req = ntr.group(3)
            param_type = ntr.group(7)
        else:
            raise ValueError("Invalid property format: " +
                             docname + ' - ' + node.rawsource)
            prop_name = ''

        # todo check props valid, and prop in jschema
        jprop = jschema[str(prop_name)]

        desc = markdown[markdown.index(': ') + 2:].strip()
        if param_type:
            desc = param_type + ': ' + desc

        jprop["markdownDescription"] = desc

    except Exception as e:
        print("In {}: {} cannot update prop from source: {}".format(
              docname, str(e), node.rawsource))
    return

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


def check_missing(app, jschema, component):
    props = find_props(jschema, app)
    if not props:
        print('In: {} cannot find properties'.format(component))

    for key, val in props.items():
        if not 'markdownDescription' in val:
            print('In: {} cannot find markdown description for {}'.format(
                component, key))


def test_jschema(app, exception):
    # create report of missing descriptions

    try:

        for key, val in app.jschema["properties"].items():
            # multi components?
            if '$ref' in val:
                continue
            # binary_sensor, sensor
            if 'items' in val:
                continue
            try:
                check_missing(app, val, key)
            except Exception as e:
                print('----')
                print(e)
                print('checking missing key {}: {}'.format(
                    key, json.dumps(val)[:100]))

    except Exception as e:
        print(e)

    f = open(SCHEMA_PATH, 'w', encoding="utf-8-sig")
    f.write(json.dumps(app.jschema))
