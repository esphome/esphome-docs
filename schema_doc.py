import re
import docutils
from markdown import MDWriter
import os
import xml.etree.ElementTree as ET
import json
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.core import publish_doctree, publish_file, publish_from_doctree

SCHEMA_PATH = '../esphome_devices/schema.json'
# SCHEMA_PATH = '../esphome-vscode/server/src/schema.json'


def setup(app):
    """Setup connects events to the sitemap builder"""

    app.connect('doctree-resolved', doctree_resolved)
    app.connect('build-finished', test_jschema)
    f = open(SCHEMA_PATH, 'r', encoding="utf-8-sig")
    str = f.read()
    app.jschema = json.loads(str)

    return {"version": "1.0.0",
            "parallel_read_safe": True,
            "parallel_write_safe": True}


def find_component(jschema, component):
    return jschema["properties"].get(component)


def find_platform_component(jschema, platform, component):
    platform_items = jschema["properties"][platform].get("items")
    if not platform_items:
        return None
    ar = platform_items['allOf']
    for p in ar:
        if "if" in p:
            if p["if"]["properties"]["platform"]["const"] == component:
                return p


def doctree_resolved(app, doctree, docname):
    if docname == 'components/index':
        # nothing useful here
        return
    try:
        handle_component(app, doctree, docname)

    except Exception as e:
        err_str = 'In {}: {}'.format(docname, str(e))
        print(err_str)


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
        if not arr:
            if '$ref' in node:
                return find_props(get_ref(app.jschema, node), app)
            return None
        for x in arr:
            props = x.get('properties')
            if not ref:
                ref = get_ref(app.jschema, x)
            if props:
                break
    if not props and ref:
        return find_props(ref, app)

    return props


PLATFORMS_TITLES = {'Sensor': 'sensor',
                    'Binary Sensor': 'binary_sensor',
                    'Output': 'output',
                    'Cover': 'cover',
                    'CAN Bus': 'canbus',
                    'Stepper': 'stepper'}

CUSTOM_DOCS = {
    'guides/automations': {
        'Global Variables': 'globals'
    },
    'guides/configuration-types': {
        'Color': 'color'
    },
    'components/display/index': {
        'Images': 'image',
        'Drawing Static Text': 'font',
        'Animation': 'animation'
    },
    'custom/custom_component': {
        'Generic Custom Component': 'custom_component'
    },
}


def handle_component(app, doctree, docname):
    path = docname.split('/')
    json_component = None
    props = None
    component = None
    platform = None
    json_platform_component = None
    json_base_config = None
    if path[0] == 'components':
        if len(path) == 2:  # root component, e.g. dfplayer, logger
            component = docname[11:]
            json_component = app.jschema["properties"].get(component)
        else:  # sub component, e.g. output/esp8266_pwm

            # components here might have a core / hub, eg. dallas, ads1115
            # and then they can be a binary_sensor, sensor, etc.

            component = path[2]

            if component == 'ssd1331':
                component = 'ssd1331_spi'

            platform = path[1]
            if component == 'index':
                # these are e.g. sensor, binary sensor etc.
                p = platform.replace(' ', '_').lower()
                json_component = find_component(app.jschema, platform)
                json_base_config = app.jschema["definitions"].get(
                    p + '.' + p.upper() + '_SCHEMA')

            else:
                json_component = find_component(app.jschema, component)

                json_platform_component = find_platform_component(
                    app.jschema, platform, component)

    elif docname not in CUSTOM_DOCS:
        return

    # ESPHome page docs follows strict formating guidelines which allows
    # for docs to be parsed directly into yaml schema

    # Document first paragraph is description of this thing
    description = getMarkdownParagraph(app, docname, doctree, doctree)
    if json_component:
        json_component["markdownDescription"] = description
    elif json_platform_component:
        json_platform_component["markdownDescription"] = description

    if json_base_config:
        json_component = json_base_config

    updated_props = 0

    # for most components / platforms get the props, this allows for a less restrictive
    # first title on the page
    if json_component or json_platform_component:
        props = find_props(
            json_component if json_component else json_platform_component, app)

        if not props:
            # get props for base components, Sensor, Binary Sensor, Light, etc.

            if len(path) == 2:
                # "#/definitions/schema_canbus.CONFIG_SCHEMA"
                c_s = app.jschema["definitions"].get(
                    "{}.{}_SCHEMA".format(path[1], path[1].upper()))
                if c_s:
                    props = find_props(c_s, app)

    custom_doc = CUSTOM_DOCS.get(docname)

    title_text = 'No title'

    is_component_hub = False

    for section in doctree.traverse(nodes.section):
        # First title is the component title, e.g.
        # components/ads1115.rst ADS115 Sensor
        # Second title must be 'Component/Hub' for components with both
        # json_component and json_schema, these are components with hub
        title = section.next_node(nodes.Titular)
        if not title:
            continue
        previous_title = title_text
        title_text = title.astext()

        if custom_doc is not None and title_text in custom_doc:
            component_name = custom_doc[title_text]
            json_component = app.jschema["properties"][component_name]
            props = find_props(json_component, app)

            json_component["markdownDescription"] = getMarkdownParagraph(
                app, docname, doctree, section)
            continue

        if title_text == 'Component/Hub':
            # here comes docs for the component, make sure we have props of the component
            # Needed for e.g. ads1115
            json_component = find_component(app.jschema, component)
            if json_component:
                props = find_props(json_component, app)
            # mark this to retrieve components instead of platforms
            is_component_hub = True
        if title_text == "Configuration variables:":
            if not props:
                raise ValueError(
                    'In {} Found a Configuration variables: title after "{}". Unkown object.'.format(
                        docname, previous_title))
            # This is a section of configuration, update props with this section
            for config in title.traverse(nodes.list_item, siblings=True):
                key = list(config.traverse(nodes.Text))[0].astext()
                if key in props:
                    if 'brightness' in key:
                        key = key
                    update_prop(app, doctree, docname, config, props)
                    updated_props = updated_props + 1
            props = None
        if title_text == 'Over SPI' or title_text == 'Over I²C':
            suffix = '_spi' if 'SPI' in title_text else '_i2c'

            # these could be platform components, like the display's ssd1306
            # but also there are components which are component/hub
            # and there are non platform components with the SPI/I2C versions,
            # like pn532, those need to be marked with the 'Component/Hub' title

            if platform is not None and not is_component_hub:
                json_platform_component = find_platform_component(app.jschema,
                                                                  platform, component + suffix)
                if not json_platform_component:
                    raise ValueError("Cannot find platform {} component '{}' after found title: '{}'.".format(
                        platform, component + suffix, title_text
                    ))
                props = find_props(json_platform_component, app)

                # Document first paragraph is description of this thing
                json_platform_component["markdownDescription"] = getMarkdownParagraph(app, docname, doctree,
                                                                                      section)

            else:
                json_component = find_component(
                    app.jschema, component + suffix)
                if not json_component:
                    raise ValueError("Cannot find component '{}' after found title: '{}'.".format(
                        component + suffix, title_text
                    ))
                props = find_props(json_component, app)

                # Document first paragraph is description of this thing
                json_component["markdownDescription"] = getMarkdownParagraph(app, docname, doctree,
                                                                             section)

        # Title is description of platform component, those ends with Sensor, Binary Sensor, Cover, etc.
        if (len(list(filter(lambda x: title_text.endswith(x), list(PLATFORMS_TITLES.keys())))) > 0):
            if title_text in PLATFORMS_TITLES:
                # this omits the name of the component, but we know the platform
                platform_name = PLATFORMS_TITLES[title_text]
                component_name = component
            else:
                # title first word is the component name
                component_name = title_text.split(' ')[0]
                # and the rest is the platform
                platform_name = PLATFORMS_TITLES.get(
                    title_text[len(component_name) + 1:])
                if not platform_name:
                    # Some general title which does not locate a component directly
                    continue

            c = find_platform_component(
                app.jschema, platform_name, component_name.lower())
            if c:
                json_platform_component = c

            # Now fill props for the platform element
            try:
                props = find_props(json_platform_component, app)
            except:
                raise ValueError(
                    'Cannot find platform props'.format(docname))

        if title_text.endswith('Component') or title_text.endswith('Bus'):
            # if len(path) == 3 and path[2] == 'index':
            #     # skip platforms index, e.g. sensors/index
            #     continue
            split_text = title_text.split(' ')
            if len(split_text) == 2:
                # some components are several components in a single platform doc
                # e.g. ttp229 binary_sensor has two different named components.
                component_name = split_text[0].lower()
                if component_name.lower() == platform:
                    continue
                c = find_component(
                    app.jschema, component_name)
                if c:
                    json_component = c
                    try:
                        props = find_props(json_component, app)
                    except:
                        raise ValueError(
                            'Cannot find props for component ' + component_name)
                    continue
                c = find_platform_component(
                    app.jschema, path[1], component_name)
                if c:
                    json_platform_component = c
                    try:
                        props = find_props(json_platform_component, app)
                    except:
                        raise ValueError(
                            'Cannot find props for platform {} component {}'.format(path[1], component_name))
                    continue

    if updated_props == 0 and 'No configuration variables.' not in doctree.astext():
        print('No updated props from ' + docname)


def getMarkdown(app, docname, doctree, node):
    from urllib import parse
    from markdown import Translator
    t = Translator(parse.urljoin(
        app.config.html_baseurl, docname + '.html'), doctree)
    node.walkabout(t)
    return t.output


def getMarkdownParagraph(app, docname, doctree, paragraph):
    node = list(paragraph.traverse(nodes.paragraph))[0]
    return getMarkdown(app, docname, doctree, node)


def update_prop(app, doctree, docname, node, jschema):
    try:

        markdown = getMarkdown(app, docname, doctree, node)

        raw = node.rawsource  # this has the full raw rst code for this property

        sep_idx = raw.replace('\n', ' ').index(': ')
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


# def add_html_link(app, pagename, templatename, context, doctree):
#     print('add_html_link: ' + str(pagename))


NOT_DOCUMENTED = ['web_server_base']

IGNORE_MISSING_KEYS = ['id', 'web_server_base_id', 'raw_data_id', 'time_id',
                       'one_wire_id']


def check_missing(app, jschema, component):
    if component in NOT_DOCUMENTED:
        return
    props = find_props(jschema, app)
    if not props:
        print('In: {} cannot find properties'.format(component))
        return

    for key, val in props.items():
        if not 'markdownDescription' in val and not key in IGNORE_MISSING_KEYS:
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
                print('In: {} error: {}'.format(key, str(e)))

    except Exception as e:
        print(e)

    f = open(SCHEMA_PATH, 'w', encoding="utf-8-sig")
    f.write(json.dumps(app.jschema))
