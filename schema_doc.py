from typing import MutableMapping
from sphinx.util import logging
import re
from types import TracebackType
import docutils
from markdown import MDWriter
import os
import xml.etree.ElementTree as ET
import json
import traceback
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.core import publish_doctree, publish_file, publish_from_doctree

SCHEMA_PATH = '../esphome_devices/schema.json'
# SCHEMA_PATH = '../esphome-vscode/server/src/schema.json'

props_missing = 0
props_verified = 0
props_documented = 0


def setup(app):
    """Setup connects events to the sitemap builder"""

    app.connect('doctree-resolved', doctree_resolved)
    app.connect('build-finished', build_finished)
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

        err_str = f'In {docname}: {str(e)}'

        logger = logging.getLogger(__name__)
        logger.warning(err_str)

        traceback.print_exc()
        # print(err_str)


PLATFORMS_TITLES = {'Sensor': 'sensor',
                    'Binary Sensor': 'binary_sensor',
                    'Text Sensor': 'text_sensor',
                    'Output': 'output',
                    'Cover': 'cover',
                    'Climate': 'climate',
                    'CAN Bus': 'canbus',
                    'Stepper': 'stepper'}

CUSTOM_DOCS = {
    'guides/automations': {
        'Global Variables': 'properties/globals'
    },
    'guides/configuration-types': {
        'Color': 'properties/color',
        'Pin Schema': 'definitions/PIN.GPIO_FULL_INPUT_PIN_SCHEMA'
    },
    'components/climate/ir_climate': {
        'IR Remote Climate': [
            'properties/climate/coolix',
            'properties/climate/daikin',
            'properties/climate/fujitsu_general',
            'properties/climate/mitsubishi',
            'properties/climate/tcl112',
            'properties/climate/toshiba',
            'properties/climate/yashima',
            'properties/climate/whirlpool',
            'properties/climate/climate_ir_lg',
            'properties/climate/hitachi_ac344',
        ]
    },
    'components/display/index': {
        'Images': 'properties/image',
        'Drawing Static Text': 'properties/font',
        'Color': 'properties/color',
        'Animation': 'properties/animation'
    },
    'components/light/index': {
        'Base Light Configuration': [
            'definitions/light.ADDRESSABLE_LIGHT_SCHEMA',
            'definitions/light.BINARY_LIGHT_SCHEMA',
            'definitions/light.BRIGHTNESS_ONLY_LIGHT_SCHEMA',
            'definitions/light.LIGHT_SCHEMA',
        ]
    },
    'components/light/fastled': {
        'Clockless': 'properties/light/fastled_clockless',
        'SPI': 'properties/light/fastled_spi'
    },
    'components/mqtt': {
        'MQTT Component Base Configuration': 'definitions/CONFIG.MQTT_COMMAND_COMPONENT_SCHEMA',
    },
    'components/output/index': {
        'Base Output Configuration': 'definitions/output.FLOAT_OUTPUT_SCHEMA'
    },
    'components/remote_transmitter': {
        'Remote Transmitter Actions':  'definitions/REMOTE_BASE.BASE_REMOTE_TRANSMITTER_SCHEMA'
    },
    'components/time': {
        'Home Assistant Time Source': 'properties/time/homeassistant',
        'SNTP Time Source': 'properties/time/sntp',
        'GPS Time Source': 'properties/time/gps',
        'DS1307 Time Source': 'properties/time/ds1307',
    },
    'components/wifi': {
        'Connecting to Multiple Networks': 'definitions/wifi-networks',
        'Enterprise Authentication': 'definitions/wifi-networks/eap'
    },
    'custom/custom_component': {
        'Generic Custom Component': 'properties/custom_component'
    },

}


class SchemaGeneratorVisitor(nodes.NodeVisitor):
    def __init__(self, app, doctree, docname):
        nodes.NodeVisitor.__init__(self, doctree)
        self.app = app
        self.doctree = doctree
        self.docname = docname
        self.path = docname.split('/')
        self.json_component = None
        self.props = None
        self.platform = None
        self.json_platform_component = None
        self.json_base_config = None
        if self.path[0] == 'components':
            if len(self.path) == 2:  # root component, e.g. dfplayer, logger
                component = docname[11:]
                self.json_component = app.jschema["properties"].get(component)
            else:  # sub component, e.g. output/esp8266_pwm

                # components here might have a core / hub, eg. dallas, ads1115
                # and then they can be a binary_sensor, sensor, etc.

                component = self.path[2]

                if component == 'ssd1331':
                    component = 'ssd1331_spi'

                self.platform = self.path[1]
                if component == 'index':
                    # these are e.g. sensor, binary sensor etc.
                    p = self.platform.replace(' ', '_').lower()
                    self.json_component = find_component(
                        self.app.jschema, self.platform)
                    self.json_base_config = self.app.jschema["definitions"].get(
                        p + '.' + p.upper() + '_SCHEMA')

                else:
                    self.json_component = find_component(
                        self.app.jschema, component)

                    self.json_platform_component = find_platform_component(
                        self.app.jschema, self.platform, component)

        self.custom_doc = CUSTOM_DOCS.get(docname)

        self.previous_title_text = 'No title'

        self.is_component_hub = False

        # used in custom_docs when titles are mapped to array of components, this
        # allows for same configuration text be applied to different json schemas
        self.multi_component = None

        # a stack for props, used when there are nested props to save high level props.
        self.prop_stack = []

        # The prop just filled in, used when there are nested props and need to know which
        # want to dig
        self.current_prop = None

        # self.filled_props used to know when any prop is added to props,
        # we dont invalidate props on exiting bullet lists but just when entering a new title
        self.filled_props = False

        # Found a Configuration variables: heading, this is to increase docs consistency
        self.accept_props = False

        self.props_level = 0

    def visit_document(self, node):
        # ESPHome page docs follows strict formating guidelines which allows
        # for docs to be parsed directly into yaml schema

        if self.docname in ['components/sensor/binary_sensor_map']:
            # temporarly not supported
            raise nodes.SkipChildren

        if len(list(node.traverse(nodes.paragraph))) == 0:
            # this is empty, not much to do
            raise nodes.SkipChildren

        # Document first paragraph is description of this thing
        description = self.getMarkdownParagraph(node)

        if self.json_platform_component:
            self.json_platform_component["markdownDescription"] = description
        elif self.json_component:
            self.json_component["markdownDescription"] = description

        if self.json_base_config:
            self.json_component = self.json_base_config

        # for most components / platforms get the props, this allows for a less restrictive
        # first title on the page
        if self.json_component or self.json_platform_component:
            self.props = self.find_props(
                self.json_platform_component if self.json_platform_component else self.json_component)

            if not self.props:
                # get props for base components, Sensor, Binary Sensor, Light, etc.

                if len(self.path) == 2:
                    # "#/definitions/schema_canbus.CONFIG_SCHEMA"
                    self.json_base_config = self.app.jschema["definitions"].get(
                        f"{self.path[1]}.{self.path[1].upper()}_SCHEMA")
                    if self.json_base_config:
                        self.props = self.find_props(self.json_base_config)

    def depart_document(self, node):
        pass

    def visit_SEONode(self, node):
        pass

    def depart_SEONode(self, node):
        pass

    def visit_literal_block(self, node):
        pass

    def depart_literal_block(self, node):
        pass

    def visit_section(self, node):
        pass

    def depart_section(self, node):
        pass

    def unknown_visit(self, node):
        pass

    def unknown_departure(self, node):
        pass

    def visit_title(self, node):
        title_text = node.astext()

        if 'interval' in title_text:
            title_text = title_text
        if self.custom_doc is not None and title_text in self.custom_doc:
            if isinstance(self.custom_doc[title_text], list):
                self.multi_component = self.custom_doc[title_text]

                # TODO: add same markdown description to each?

                return
            json_component = self.find_component(self.custom_doc[title_text])
            json_component["markdownDescription"] = self.getMarkdownParagraph(
                node.parent)

            self.props = self.find_props(json_component)

            return

        if title_text == 'Component/Hub':
            # here comes docs for the component, make sure we have props of the component
            # Needed for e.g. ads1115
            json_component = find_component(self.app.jschema, self.path[-1])
            if json_component:
                self.props = self.find_props(json_component)
            # mark this to retrieve components instead of platforms
            self.is_component_hub = True

        if title_text == "Configuration variables:":
            if not self.props and self.multi_component == None:
                raise ValueError(
                    f'Found a Configuration variables: title after {self.previous_title_text}. Unkown object.')

        if title_text == 'Over SPI' or title_text == 'Over I²C':
            suffix = '_spi' if 'SPI' in title_text else '_i2c'

            # these could be platform components, like the display's ssd1306
            # but also there are components which are component/hub
            # and there are non platform components with the SPI/I2C versions,
            # like pn532, those need to be marked with the 'Component/Hub' title
            component = self.path[-1] + suffix

            if self.platform is not None and not self.is_component_hub:
                json_platform_component = find_platform_component(self.app.jschema,
                                                                  self.platform, component)
                if not json_platform_component:
                    raise ValueError(
                        f"Cannot find platform {self.platform} component '{component}' after found title: '{title_text}'.")
                self.props = self.find_props(json_platform_component)

                # Document first paragraph is description of this thing
                json_platform_component["markdownDescription"] = self.getMarkdownParagraph(
                    node.parent)

            else:
                json_component = find_component(
                    self.app.jschema, component)
                if not json_component:
                    raise ValueError(
                        f"Cannot find component '{component}' after found title: '{title_text}'.")
                self.props = self.find_props(json_component)

                # Document first paragraph is description of this thing
                json_component["markdownDescription"] = self.getMarkdownParagraph(
                    node.parent)

        # Title is description of platform component, those ends with Sensor, Binary Sensor, Cover, etc.
        if (len(list(filter(lambda x: title_text.endswith(x), list(PLATFORMS_TITLES.keys())))) > 0):
            if title_text in PLATFORMS_TITLES:
                # this omits the name of the component, but we know the platform
                platform_name = PLATFORMS_TITLES[title_text]
                component_name = self.path[-1]
            else:
                # title first word is the component name
                component_name = title_text.split(' ')[0]
                # and the rest is the platform
                platform_name = PLATFORMS_TITLES.get(
                    title_text[len(component_name) + 1:])
                if not platform_name:
                    # Some general title which does not locate a component directly
                    return

            c = find_platform_component(
                self.app.jschema, platform_name, component_name.lower())
            if c:
                self.json_platform_component = c

            # Now fill props for the platform element
            try:
                self.props = self.find_props(self.json_platform_component)

            except:
                raise ValueError('Cannot find platform props')

        if title_text.endswith('Component') or title_text.endswith('Bus'):
            # if len(path) == 3 and path[2] == 'index':
            #     # skip platforms index, e.g. sensors/index
            #     continue
            split_text = title_text.split(' ')
            if len(split_text) == 2:
                # some components are several components in a single platform doc
                # e.g. ttp229 binary_sensor has two different named components.
                component_name = split_text[0].lower().replace('.', '')
                if component_name.lower() == self.platform:
                    return
                c = find_component(
                    self.app.jschema, component_name)
                if c:
                    self.json_component = c
                    try:
                        self.props = self.find_props(self.json_component)
                    except:
                        raise ValueError(
                            'Cannot find props for component ' + component_name)
                    return
                c = find_platform_component(
                    self.app.jschema, self.path[1], component_name)
                if c:
                    self.json_platform_component = c
                    try:
                        self.props = self.find_props(
                            self.json_platform_component)

                    except:
                        raise ValueError(
                            f'Cannot find props for platform {self.path[1]} component {self.component_name}')
                    return

        if title_text.endswith('Action') or title_text.endswith('Condition'):
            # Document first paragraph is description of this thing
            description = self.getMarkdownParagraph(node.parent)
            split_text = title_text.split(' ')
            if len(split_text) != 2:
                return
            key = split_text[0]
            registry_name = f"automation.{split_text[1].upper()}_REGISTRY"
            registry = self.app.jschema["definitions"][registry_name]["anyOf"]
            for action in registry:
                if key in action["properties"]:
                    action["properties"][key]["markdownDescription"] = description
                    self.props = self.find_props(action["properties"][key])
                    break

        if title_text.endswith('Trigger'):
            # Document first paragraph is description of this thing
            description = self.getMarkdownParagraph(node.parent)
            split_text = title_text.split(' ')
            if len(split_text) != 2:
                return
            key = split_text[0]

            # handles Time / on_time
            c = self.json_base_config or self.json_component
            if c:
                trigger_schema = self.find_props(c).get(key)
                self.props = self.find_props(trigger_schema)

        if self.docname == 'components/light/index' and title_text.endswith('Effect'):
            # Document first paragraph is description of this thing

            description = self.getMarkdownParagraph(node.parent)
            name = title_text[:-len(' Effect')]
            # accept Light Effect as ending (Automation Light Effect)
            if name.endswith(' Light'):
                name = name[:-len(' Light')]

            key = name.replace(' ', '_').replace('.', '').lower()
            registry = self.app.jschema["definitions"]["light.EFFECTS_REGISTRY"]["anyOf"]
            for effect in registry:
                if key in effect["properties"]:
                    effect["properties"][key]["markdownDescription"] = description
                    self.props = self.find_props(effect["properties"][key])
                    return
            raise ValueError('Cannot find Effect ' + title_text)

    def depart_title(self, node):
        if self.filled_props:
            self.filled_props = False
            self.props = None
            self.current_prop = None
            self.accept_props = False
            self.multi_component = None
        self.previous_title_text = node.astext()

    def find_props_previous_title(self):
        comp = self.json_component or self.json_platform_component
        if comp:
            props = self.find_props(comp)

            if self.previous_title_text in props:
                prop = props[self.previous_title_text]
                if prop:
                    self.props = self.find_props(prop)
                else:
                    # return fake dict so better errors are printed
                    self.props = {'__': 'none'}

    def visit_Text(self, node):
        if self.multi_component:
            return
        if node.astext() == "Configuration variables:":
            if not self.props:
                self.find_props_previous_title()
            if not self.props:
                raise ValueError(
                    f'Found a "Configuration variables:" entry for unknown object after {self.previous_title_text}')
            self.accept_props = True
        raise nodes.SkipChildren

    def depart_Text(self, node):
        pass

    def visit_paragraph(self, node):
        if node.astext() == "Configuration variables:":
            if not self.props:
                self.find_props_previous_title()
            if not self.props:
                raise ValueError(
                    f'Found a "Configuration variables:" entry for unknown object after {self.previous_title_text}')
            self.accept_props = True
        raise nodes.SkipChildren

    def depart_paragraph(self, node):
        pass

    def visit_bullet_list(self, node):
        self.props_level = self.props_level + 1
        if self.current_prop and self.props and self.props_level > 1:

            # if '$ref' in self.props[self.current_prop]:
            #     if self.props[self.current_prop]['$ref'].endswith('_SCHEMA'):
            # nowhere put this props info...
            # raise nodes.SkipChildren

            # this can be list of values, list of subproperties

            # deep configs
            # e.g. wifi manual_ip, could also be a enum list

            # if this prop has a reference
            prop = self.props[self.current_prop]
            if isinstance(prop, dict):
                if '$ref' in prop:
                    ref = self.get_ref(prop)
                    self.prop_stack.append(self.props)
                    self.props = self.find_props(ref)
                    self.accept_props = True
                elif 'properties' in prop:
                    self.prop_stack.append(self.props)
                    self.props = prop['properties']
                elif 'anyOf' in prop and len(prop['anyOf']) > 0 \
                        and isinstance(self.get_ref(prop['anyOf'][0]), dict) \
                        and '$ref' in self.get_ref(prop['anyOf'][0]):
                    ref = self.get_ref(prop['anyOf'][0])
                    self.prop_stack.append(self.props)
                    self.props = self.find_props(ref)
                # nowhere put this props info...
                # otherwise inner bullet list will be interpreted as property list
                if self.props_level > 1:
                    raise nodes.SkipChildren
            else:
                # nowhere put this props info...
                # otherwise inner bullet list will be interpreted as property list
                if self.props_level > 1:
                    raise nodes.SkipChildren

        if not self.props and self.multi_component == None:
            raise nodes.SkipChildren

    def depart_bullet_list(self, node):
        self.props_level = self.props_level - 1
        if len(self.prop_stack) > 0:
            self.props = self.prop_stack.pop()
            self.filled_props = True

    def visit_list_item(self, node):
        if self.accept_props and self.props:
            self.filled_props = True
            try:
                self.current_prop = self.update_prop(node, self.props)
                # print(
                #     f'{self.current_prop} updated from {node.rawsource[:40]}')
            except Exception as e:
                raise ValueError(
                    f"In '{self.previous_title_text}' {str(e)}")

        elif self.multi_component:
            # update prop for each component
            for c in self.multi_component:
                props = self.find_props(self.find_component(c))
                self.current_prop = self.update_prop(node, props)
            self.filled_props = True

    def depart_list_item(self, node):
        pass

    def visit_literal(self, node):
        raise nodes.SkipChildren

    def depart_literal(self, node):
        pass

    def getMarkdown(self, node):
        from urllib import parse
        from markdown import Translator
        t = Translator(parse.urljoin(
            self.app.config.html_baseurl, self.docname + '.html'), self.doctree)
        node.walkabout(t)
        return t.output

    def getMarkdownParagraph(self, paragraph):
        node = list(paragraph.traverse(nodes.paragraph))[0]
        return self.getMarkdown(node)

    def update_prop(self, node, props):
        prop_name = None

        raw = node.rawsource  # this has the full raw rst code for this property

        if not raw.startswith('**'):
            # not bolded, most likely not a property definition,
            # usually texts like 'All properties from...' etc
            return None

        markdown = self.getMarkdown(node)

        try:
            name_type = markdown[:markdown.index(': ') + 2]
        except:
            raise ValueError(f'Property format error. Missing ": " in {raw}')

        # Example properties formats are:
        # **name** (**Required**, string): Long Description...
        # **name** (*Optional*, string): Long Description... Defaults to ``value``.
        # **name** (*Optional*): Long Description... Defaults to ``value``.

        if 'ads111' in self.docname:
            self.docname = self.docname

        ntr = re.search(
            '\* \*\*(\w*)\*\*\s(\(((\*\*Required\*\*)|(\*Optional\*))(,\s(.*))*)\):\s', name_type, re.IGNORECASE)

        if ntr:
            prop_name = ntr.group(1)
            req = ntr.group(3)
            param_type = ntr.group(7)
        else:
            s2 = re.search(
                '\* \*\*(\w*)\*\*\s(\(((\*\*Required\*\*)|(\*Optional\*))(,\s(.*))*)\):\s', markdown, re.IGNORECASE)
            if s2:
                # this is e.g. when a property has a list inside, and the list inside are the options.
                # just validate **prop_name**
                s3 = re.search('\* \*\*(\w*)\*\*:\s', name_type)
                prop_name = s3.group(1)
                param_type = None
            else:
                raise ValueError(f"Invalid property format: " + node.rawsource)

        k = str(prop_name)
        jprop = props.get(k)
        if not jprop:

            # do not fail for common properties,
            # however this should check prop is valid upstream

            if k in ['id', 'name', 'internal',
                     # i2c
                     'address', 'i2c_id',
                     # polling component
                     'update_interval',
                     # uart
                     'uart_id',
                     # ligth
                     'effects', 'gamma_correct', 'default_transition_length', 'color_correct',
                     # display
                     'lambda', 'dither', 'pages', 'rotation',
                     # spi
                     'spi_id', 'cs_pin',
                     # output (binary/float output)
                     'inverted', 'power_supply',
                     # climate
                     'receiver_id']:
                return
            else:
                raise ValueError(
                    f'Cannot find property {k}')

        desc = markdown[markdown.index(': ') + 2:].strip()
        if param_type:
            desc = param_type + ': ' + desc

        if '$ref' in jprop:
            self.get_ref(jprop)["markdownDescription"] = desc
        else:
            jprop["markdownDescription"] = desc
        global props_documented
        props_documented = props_documented + 1

        return prop_name

    def get_ref(self, node):
        ref = node.get('$ref')
        if ref and ref.startswith('#/definitions/'):
            return self.app.jschema["definitions"][ref[14:]]

    def find_component(self, component_path):
        path = component_path.split('/')
        json_component = self.app.jschema[path[0]
                                          ][path[1]]

        if len(path) > 2:
            # a property path
            props = self.find_props(json_component)
            if props:
                json_component = props.get(path[2])
            else:
                # a platform sub element
                json_component = find_platform_component(
                    self.app.jschema, path[1], path[2])
        return json_component

    class Props(MutableMapping):
        # Props are mostly a dict, however some constructs have two issues:
        # - An update is intended on an element which does not own a property, but it is based
        #   on an schema that does have the property, those cases can be handled
        # - An update is done in a typed schema

        def __init__(self, visitor, component):
            self.visitor = visitor
            self.component = component
            self.store = self._get_props(component)
            self.parent = None

        def _get_props(self, component):
            # find properties
            if "then" in component:
                component = component["then"]
            props = component.get("properties")
            ref = None
            if not props:
                arr = component.get('anyOf', component.get('allOf'))
                if not arr:
                    if '$ref' in component:
                        return self._get_props(self.visitor.get_ref(component))
                    return None
                for x in arr:
                    props = x.get('properties')
                    if not ref:
                        ref = self.visitor.get_ref(x)
                    if props:
                        break
            if not props and ref:
                props = self._get_props(ref)
            return props

        def __getitem__(self, key):
            if key in self.store:
                return self.store[key]

            if "then" in self.component:
                # check if it's typed
                schemas = self.component["then"].get('allOf')
                if isinstance(schemas, list) and 'properties' in schemas[0] and 'type' in schemas[0]['properties']:
                    for s in schemas:
                        if 'then' in s:
                            props = self._get_props(s.get('then'))
                            if key in props:
                                return SetObservable(props[key], setitem_callback=self._update_typed, inner_key=key)
                    return  # key not found

                # check if it's a registry and need to reset store
                # e.g. remote_receiver binary sensor
                if '$ref' in self.component["then"]:
                    ref = self.visitor.get_ref(self.component["then"])
                    prop_set = ref.get('anyOf')
                    if isinstance(prop_set, list):
                        for k in prop_set:
                            if key in k['properties']:
                                self.store = k['properties']
                                return self.store[key]

        def _update_typed(self, inner_key, key, value):
            # Make sure we update all types
            if "then" in self.component:
                schemas = self.component["then"].get('allOf')
                assert 'type' in schemas[0].get('properties')
                for s in schemas:
                    if 'then' in s:
                        props = self._get_props(s.get('then'))
                        if inner_key in props:
                            props[inner_key][key] = value

        def __setitem__(self, key, value):
            self.store[key] = value

        def __delitem__(self, key):
            self.store.pop(key)

        def __iter__(self):
            return iter(self.store)

        def __len__(self):
            return len(self.store) if self.store else 0

    def find_props(self, component):
        props = self.Props(self, component)

        if props:
            self.filled_props = False
            self.accept_props = False
            self.current_prop = None

        return props
        return
        # find properties
        if "then" in component:
            component = component["then"]
        props = component.get("properties")
        ref = None
        if not props:
            arr = component.get('anyOf', component.get('allOf'))
            if not arr:
                if '$ref' in component:
                    return self.find_props(self.get_ref(component))
                return None
            for x in arr:
                props = x.get('properties')
                if not ref:
                    ref = self.get_ref(x)
                if props:
                    break
        if not props and ref:
            props = self.find_props(ref)

        if props:
            self.filled_props = False
            self.accept_props = False
            self.current_prop = None
        return props


def handle_component(app, doctree, docname):
    path = docname.split('/')
    if path[0] == 'components':
        pass
    elif docname not in CUSTOM_DOCS:
        return

    v = SchemaGeneratorVisitor(app, doctree, docname)
    doctree.walkabout(v)


NOT_DOCUMENTED = ['web_server_base']

IGNORE_MISSING_KEYS = ['id', 'web_server_base_id', 'raw_data_id', 'time_id',
                       'one_wire_id', 'trigger_id', 'then']


def check_missing(app, jschema, component):
    global props_missing, props_verified

    if component in NOT_DOCUMENTED:
        return
    # props = find_props(jschema, app)
    # if not props:
    #     print(f'In: {component} cannot find properties')
    #     return

    # for key, val in props.items():
    #     if not 'markdownDescription' in val and not key in IGNORE_MISSING_KEYS:
    #         print(f'In: {component} cannot find markdown description for {key}')
    #         props_missing = props_missing + 1
    #     else:
    #         props_verified = props_verified + 1


def test_schema(app):
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
                print(f'In: properties/{key} error: {str(e)}')

        for key, val in app.jschema["definitions"].items():
            # multi components?
            if '$ref' in val:
                continue
            # binary_sensor, sensor
            if 'items' in val:
                continue
            try:
                check_missing(app, val, key)
            except Exception as e:
                print(f'In: definitions/{key} error: {str(e)}')

    except Exception as e:
        print(e)


def build_finished(app, exception):
    # create report of missing descriptions
    # test_schema(app)

    f = open(SCHEMA_PATH, 'w')
    f.write(json.dumps(app.jschema))

    print('----')
    print(
        f'Documented: {props_documented} verified: {props_verified} missing: {props_missing}')


class SetObservable(dict):

    """
    a MyDict is like a dict except that when you set an item, before
    doing so it will call a callback function that was passed in when the
    MyDict instance was created
    """

    def __init__(self, value, setitem_callback=None, inner_key=None, *args, **kwargs):
        super(SetObservable, self).__init__(value, *args, **kwargs)
        self._setitem_callback = setitem_callback
        self.inner_key = inner_key

    def __setitem__(self, key, value):
        if self._setitem_callback:
            self._setitem_callback(self.inner_key, key, value)
        super(SetObservable, self).__setitem__(key, value)
