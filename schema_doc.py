import re
import json
import urllib

from typing import MutableMapping
from sphinx.util import logging
from docutils import nodes

SCHEMA_PATH = "schema.json"
CONFIGURATION_VARIABLES = "Configuration variables:"
PIN_CONFIGURATION_VARIABLES = "Pin configuration variables:"
COMPONENT_HUB = "Component/Hub"

props_missing = 0
props_verified = 0
props_documented = 0


def setup(app):
    """Setup connects events to the sitemap builder"""

    import os

    if not os.path.isfile(SCHEMA_PATH):
        logger = logging.getLogger(__name__)
        logger.info(f"{SCHEMA_PATH} not found. Not documenting schema.")
    else:
        app.connect("doctree-resolved", doctree_resolved)
        app.connect("build-finished", build_finished)

        f = open(SCHEMA_PATH, "r", encoding="utf-8-sig")
        str = f.read()
        app.jschema = json.loads(str)

    return {"version": "1.0.0", "parallel_read_safe": True, "parallel_write_safe": True}


def find_component(jschema, component):
    return jschema["properties"].get(component)


def find_platform_component(jschema, platform, component):
    platform_items = jschema["properties"][platform].get("items")
    if not platform_items:
        return None
    ar = platform_items["allOf"]
    for p in ar:
        if "if" in p:
            if p["if"]["properties"]["platform"]["const"] == component:
                return p


def doctree_resolved(app, doctree, docname):
    if docname == "components/index":
        # nothing useful here
        return
    try:
        handle_component(app, doctree, docname)

    except Exception as e:
        err_str = f"In {docname}: {str(e)}"
        logger = logging.getLogger(__name__)
        logger.warning(err_str)


PLATFORMS_TITLES = {
    "Sensor": "sensor",
    "Binary Sensor": "binary_sensor",
    "Text Sensor": "text_sensor",
    "Output": "output",
    "Cover": "cover",
    "Climate": "climate",
    "CAN Bus": "canbus",
    "Stepper": "stepper",
}

CUSTOM_DOCS = {
    "guides/automations": {
        "Global Variables": "properties/globals",
    },
    "guides/configuration-types": {
        "Color": "properties/color",
        "Pin Schema": [
            "definitions/PIN.INPUT_INTERNAL",
            "definitions/PIN.OUTPUT_INTERNAL",
        ],
    },
    "components/binary_sensor/index": {
        "Binary Sensor Filters": "binary_sensor.FILTER_REGISTRY",
    },
    "components/climate/ir_climate": {
        "IR Remote Climate": [
            "properties/climate/coolix",
            "properties/climate/daikin",
            "properties/climate/fujitsu_general",
            "properties/climate/mitsubishi",
            "properties/climate/tcl112",
            "properties/climate/toshiba",
            "properties/climate/yashima",
            "properties/climate/whirlpool",
            "properties/climate/climate_ir_lg",
            "properties/climate/hitachi_ac344",
        ]
    },
    "components/display/index": {
        "Images": "properties/image",
        "Drawing Static Text": "properties/font",
        "Color": "properties/color",
        "Animation": "properties/animation",
    },
    "components/light/index": {
        "Base Light Configuration": [
            "definitions/light.ADDRESSABLE_LIGHT_SCHEMA",
            "definitions/light.BINARY_LIGHT_SCHEMA",
            "definitions/light.BRIGHTNESS_ONLY_LIGHT_SCHEMA",
            "definitions/light.LIGHT_SCHEMA",
        ],
        "Light Effects": "light.EFFECTS_REGISTRY",
    },
    "components/light/fastled": {
        "Clockless": "properties/light/fastled_clockless",
        "SPI": "properties/light/fastled_spi",
    },
    "components/mcp230xx": {
        PIN_CONFIGURATION_VARIABLES: [
            "definitions/PIN.INPUT_mcp23xxx",
            "definitions/PIN.OUTPUT_mcp23xxx",
        ]
    },
    "components/mqtt": {
        "MQTT Component Base Configuration": "definitions/CONFIG.MQTT_COMMAND_COMPONENT_SCHEMA",
    },
    "components/output/index": {
        "Base Output Configuration": "definitions/output.FLOAT_OUTPUT_SCHEMA",
    },
    "components/remote_transmitter": {
        "Remote Transmitter Actions": "definitions/REMOTE_BASE.BASE_REMOTE_TRANSMITTER_SCHEMA",
    },
    "components/sensor/index": {
        "Sensor Filters": "sensor.FILTER_REGISTRY",
    },
    "components/time": {
        "Home Assistant Time Source": "properties/time/homeassistant",
        "SNTP Time Source": "properties/time/sntp",
        "GPS Time Source": "properties/time/gps",
        "DS1307 Time Source": "properties/time/ds1307",
    },
    "components/wifi": {
        "Connecting to Multiple Networks": "definitions/wifi-networks",
        "Enterprise Authentication": "definitions/wifi-networks/eap",
    },
    "custom/custom_component": {
        "Generic Custom Component": "properties/custom_component"
    },
}


def get_node_title(node):
    return list(node.traverse(nodes.title))[0].astext()


class SchemaGeneratorVisitor(nodes.NodeVisitor):
    def __init__(self, app, doctree, docname):
        nodes.NodeVisitor.__init__(self, doctree)
        self.app = app
        self.doctree = doctree
        self.docname = docname
        self.path = docname.split("/")
        self.json_component = None
        self.props = None
        self.platform = None
        self.json_platform_component = None
        self.json_base_config = None
        self.title_id = None
        self.props_section_title = None
        self.find_registry = None
        self.section_level = 0
        if self.path[0] == "components":
            if len(self.path) == 2:  # root component, e.g. dfplayer, logger
                component = docname[11:]
                self.json_component = app.jschema["properties"].get(component)
            else:  # sub component, e.g. output/esp8266_pwm

                # components here might have a core / hub, eg. dallas, ads1115
                # and then they can be a binary_sensor, sensor, etc.

                component = self.path[2]

                if component == "ssd1331":
                    component = "ssd1331_spi"

                self.platform = self.path[1]
                if component == "index":
                    # these are e.g. sensor, binary sensor etc.
                    p = self.platform.replace(" ", "_").lower()
                    self.json_component = find_component(
                        self.app.jschema, self.platform
                    )
                    self.json_base_config = self.app.jschema["definitions"].get(
                        p + "." + p.upper() + "_SCHEMA"
                    )

                else:
                    self.json_component = find_component(self.app.jschema, component)

                    self.json_platform_component = find_platform_component(
                        self.app.jschema, self.platform, component
                    )

        self.custom_doc = CUSTOM_DOCS.get(docname)

        self.previous_title_text = "No title"

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

        if self.docname in ["components/sensor/binary_sensor_map"]:
            # temporarly not supported
            raise nodes.SkipChildren

        if len(list(node.traverse(nodes.paragraph))) == 0:
            # this is empty, not much to do
            raise nodes.SkipChildren

        self.props_section_title = get_node_title(node)

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
                self.json_platform_component
                if self.json_platform_component
                else self.json_component
            )

            if not self.props:
                # get props for base components, Sensor, Binary Sensor, Light, etc.

                if len(self.path) == 2:
                    # "#/definitions/schema_canbus.CONFIG_SCHEMA"
                    self.json_base_config = self.app.jschema["definitions"].get(
                        f"{self.path[1]}.{self.path[1].upper()}_SCHEMA"
                    )
                    if self.json_base_config:
                        self.props = self.find_props(self.json_base_config)

    def depart_document(self, node):
        pass

    def visit_section(self, node):
        self.section_level += 1
        section_title = get_node_title(node)
        if self.custom_doc and section_title in self.custom_doc:
            r = self.custom_doc[section_title]
            if (
                isinstance(r, list)
                or r.startswith("properties")
                or r.startswith("definitions")
            ):
                return
            self.find_registry = r

    def depart_section(self, node):
        self.section_level -= 1
        if self.section_level == 1:
            self.find_registry = None

    def unknown_visit(self, node):
        pass

    def unknown_departure(self, node):
        pass

    def visit_title(self, node):
        title_text = node.astext()

        if "interval" in title_text:
            title_text = title_text
        if self.custom_doc is not None and title_text in self.custom_doc:
            if isinstance(self.custom_doc[title_text], list):
                self.multi_component = self.custom_doc[title_text]
                self.filled_props = False
                self.props = None
                # TODO: add same markdown description to each?

                return

            json_component = self.find_component(self.custom_doc[title_text])
            if not json_component:
                return

            json_component["markdownDescription"] = self.getMarkdownParagraph(
                node.parent
            )
            self.props_section_title = title_text
            self.props = self.find_props(json_component)

            return

        if title_text == COMPONENT_HUB:
            # here comes docs for the component, make sure we have props of the component
            # Needed for e.g. ads1115
            self.props_section_title = f"{self.path[-1]} {title_text}"
            json_component = find_component(self.app.jschema, self.path[-1])
            if json_component:
                self.props = self.find_props(json_component)

                json_component["markdownDescription"] = self.getMarkdownParagraph(
                    node.parent
                )

            # mark this to retrieve components instead of platforms
            self.is_component_hub = True

        if title_text == CONFIGURATION_VARIABLES:
            if not self.props and self.multi_component is None:
                raise ValueError(
                    f'Found a "{CONFIGURATION_VARIABLES}": title after {self.previous_title_text}. Unkown object.'
                )

        if title_text == "Over SPI" or title_text == "Over I²C":
            suffix = "_spi" if "SPI" in title_text else "_i2c"

            # these could be platform components, like the display's ssd1306
            # but also there are components which are component/hub
            # and there are non platform components with the SPI/I2C versions,
            # like pn532, those need to be marked with the 'Component/Hub' title
            component = self.path[-1] + suffix

            self.props_section_title = self.path[-1] + " " + title_text

            if self.platform is not None and not self.is_component_hub:
                json_platform_component = find_platform_component(
                    self.app.jschema, self.platform, component
                )
                if not json_platform_component:
                    raise ValueError(
                        f"Cannot find platform {self.platform} component '{component}' after found title: '{title_text}'."
                    )
                self.props = self.find_props(json_platform_component)

                # Document first paragraph is description of this thing
                json_platform_component[
                    "markdownDescription"
                ] = self.getMarkdownParagraph(node.parent)

            else:
                json_component = find_component(self.app.jschema, component)
                if not json_component:
                    raise ValueError(
                        f"Cannot find component '{component}' after found title: '{title_text}'."
                    )
                self.props = self.find_props(json_component)

                # Document first paragraph is description of this thing
                json_component["markdownDescription"] = self.getMarkdownParagraph(
                    node.parent
                )

        # Title is description of platform component, those ends with Sensor, Binary Sensor, Cover, etc.
        if (
            len(
                list(
                    filter(
                        lambda x: title_text.endswith(x), list(PLATFORMS_TITLES.keys())
                    )
                )
            )
            > 0
        ):
            if title_text in PLATFORMS_TITLES:
                # this omits the name of the component, but we know the platform
                platform_name = PLATFORMS_TITLES[title_text]
                component_name = self.path[-1]
                self.props_section_title = self.path[-1] + " " + title_text
            else:
                # title first word is the component name
                component_name = title_text.split(" ")[0]
                # and the rest is the platform
                platform_name = PLATFORMS_TITLES.get(
                    title_text[len(component_name) + 1 :]
                )
                if not platform_name:
                    # Some general title which does not locate a component directly
                    return
                self.props_section_title = title_text
            c = find_platform_component(
                self.app.jschema, platform_name, component_name.lower()
            )
            if c:
                self.json_platform_component = c

                c["markdownDescription"] = self.getMarkdownParagraph(node.parent)

            # Now fill props for the platform element
            try:
                self.props = self.find_props(self.json_platform_component)
            except KeyError:
                raise ValueError("Cannot find platform props")

        if title_text.endswith("Component") or title_text.endswith("Bus"):
            # if len(path) == 3 and path[2] == 'index':
            #     # skip platforms index, e.g. sensors/index
            #     continue
            split_text = title_text.split(" ")
            self.props_section_title = title_text
            if len(split_text) == 2:
                # some components are several components in a single platform doc
                # e.g. ttp229 binary_sensor has two different named components.
                component_name = split_text[0].lower().replace(".", "")
                if component_name.lower() == self.platform:
                    return
                c = find_component(self.app.jschema, component_name)
                if c:
                    self.json_component = c
                    try:
                        self.props = self.find_props(self.json_component)
                        self.multi_component = None
                    except KeyError:
                        raise ValueError(
                            "Cannot find props for component " + component_name
                        )
                    return
                c = find_platform_component(
                    self.app.jschema, self.path[1], component_name
                )
                if c:
                    self.json_platform_component = c
                    try:
                        self.props = self.find_props(self.json_platform_component)

                    except KeyError:
                        raise ValueError(
                            f"Cannot find props for platform {self.path[1]} component {self.component_name}"
                        )
                    return

        if title_text.endswith("Trigger"):
            # Document first paragraph is description of this thing
            description = self.getMarkdownParagraph(node.parent)
            split_text = title_text.split(" ")
            if len(split_text) != 2:
                return
            key = split_text[0]

            # handles Time / on_time
            c = self.json_base_config or self.json_component
            if c:
                trigger_schema = self.find_props(c).get(key)
                if trigger_schema is not None:
                    self.props = self.find_props(trigger_schema)
            self.props_section_title = title_text

        if title_text == PIN_CONFIGURATION_VARIABLES:
            self.multi_component = []
            if self.app.jschema["definitions"].get(f"PIN.INPUT_{self.path[-1]}"):
                self.multi_component.append(f"definitions/PIN.INPUT_{self.path[-1]}")
            if self.app.jschema["definitions"].get(f"PIN.OUTPUT_{self.path[-1]}"):
                self.multi_component.append(f"definitions/PIN.OUTPUT_{self.path[-1]}")
            self.accept_props = True
            self.filled_props = False
            self.props = None
            if len(self.multi_component) == 0:
                raise ValueError(
                    f'Found a "{PIN_CONFIGURATION_VARIABLES}" entry but could not find pin schema'
                )

        if title_text.endswith("Action") or title_text.endswith("Condition"):
            # Document first paragraph is description of this thing
            description = self.getMarkdownParagraph(node.parent)
            split_text = title_text.split(" ")
            if len(split_text) != 2:
                return
            key = split_text[0]

            if self.props:
                ref = self.props.get(key)
                if ref:
                    ref = self.get_ref(ref)
                    if ref:
                        self.props = self.find_props(ref)
                        return

            registry_name = f"automation.{split_text[1].upper()}_REGISTRY"
            self.find_registry_prop(registry_name, key, description)

        if self.section_level == 3 and self.find_registry:
            name = title_text
            if name.endswith(" Effect"):
                name = title_text[: -len(" Effect")]
            if name.endswith(" Light"):
                name = name[: -len(" Light")]
            key = name.replace(" ", "_").replace(".", "").lower()
            description = self.getMarkdownParagraph(node.parent)
            self.find_registry_prop(self.find_registry, key, description)
            self.props_section_title = title_text

        if title_text == PIN_CONFIGURATION_VARIABLES:
            self.multi_component = []
            if self.app.jschema["definitions"].get(f"PIN.INPUT_{self.path[-1]}"):
                self.multi_component.append(f"definitions/PIN.INPUT_{self.path[-1]}")
            if self.app.jschema["definitions"].get(f"PIN.OUTPUT_{self.path[-1]}"):
                self.multi_component.append(f"definitions/PIN.OUTPUT_{self.path[-1]}")
            self.accept_props = True
            self.filled_props = False
            self.props = None
            if len(self.multi_component) == 0:
                raise ValueError(
                    f'Found a "{PIN_CONFIGURATION_VARIABLES}" entry but could not find pin schema'
                )

    def find_registry_prop(self, registry_name, key, description):
        registry = self.app.jschema["definitions"][registry_name]["anyOf"]
        for item in registry:
            if "$ref" in item:
                item = self.get_ref(item)
            if key in item["properties"]:
                item["properties"][key]["markdownDescription"] = description
                self.props = self.find_props(item["properties"][key])

                return
        raise ValueError(f"Cannot find {registry_name} {key}")

    def depart_title(self, node):
        if self.filled_props:
            self.filled_props = False
            self.props = None
            self.current_prop = None
            self.accept_props = False
            self.multi_component = None
        self.previous_title_text = node.astext()
        self.title_id = node.parent["ids"][0]

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
                    self.props = {"__": "none"}

    def visit_Text(self, node):
        if self.multi_component:
            return
        if node.astext() == CONFIGURATION_VARIABLES:
            if not self.props:
                self.find_props_previous_title()
            if not self.props:
                raise ValueError(
                    f'Found a "{CONFIGURATION_VARIABLES}" entry for unknown object after {self.previous_title_text}'
                )
            self.accept_props = True

        raise nodes.SkipChildren

    def depart_Text(self, node):
        pass

    def visit_paragraph(self, node):
        if node.astext() == CONFIGURATION_VARIABLES:
            if not self.props and not self.multi_component:
                self.find_props_previous_title()
            if not self.props and not self.multi_component:
                raise ValueError(
                    f'Found a "{CONFIGURATION_VARIABLES}" entry for unknown object after {self.previous_title_text}'
                )
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
                if "$ref" in prop:
                    ref = self.get_ref(prop)
                    self.prop_stack.append(self.props)
                    self.props = self.find_props(ref)
                    self.accept_props = True
                elif "properties" in prop:
                    self.prop_stack.append(self.props)
                    self.props = prop["properties"]
                elif (
                    "anyOf" in prop
                    and len(prop["anyOf"]) > 0
                    and isinstance(self.get_ref(prop["anyOf"][0]), dict)
                    and "$ref" in self.get_ref(prop["anyOf"][0])
                ):
                    ref = self.get_ref(prop["anyOf"][0])
                    self.prop_stack.append(self.props)
                    self.props = self.find_props(ref)
                else:
                    # TODO: if the list items are formated like:
                    #   - ``value`` <optional description>
                    #   - ``other value`` <optional description>
                    # then we could ensure these are enum values (or populate enum values double check.)
                    # Currently some enum values are also in the **value** format.
                    if (
                        # most likely an enum, the values are most likely retrieved from ESPHome validation schema
                        "enum" in prop
                        # or custom components has list of sensors/binary sensors, etc.
                        or (
                            prop.get("markdownDescription", "").startswith("**list**")
                            and self.docname.endswith("/custom")
                        )
                    ):
                        raise nodes.SkipChildren
                    # nowhere put this props info...
                    # otherwise inner bullet list will be interpreted as property list
                    logger = logging.getLogger(__name__)
                    logger.info(
                        f"In {self.docname} / {self.previous_title_text} property {self.current_prop} a unknown info sub bullet list."
                    )
                    raise nodes.SkipChildren
            else:
                # nowhere put this props info...
                # otherwise inner bullet list will be interpreted as property list
                raise nodes.SkipChildren

        if not self.props and self.multi_component is None:
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
            except Exception as e:
                raise ValueError(f"In '{self.previous_title_text}' {str(e)}")

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
        from markdown import Translator

        t = Translator(
            urllib.parse.urljoin(self.app.config.html_baseurl, self.docname + ".html"),
            self.doctree,
        )
        node.walkabout(t)
        return t.output

    def getMarkdownParagraph(self, node):
        paragraph = list(node.traverse(nodes.paragraph))[0]
        markdown = self.getMarkdown(paragraph)

        param_type = None
        # Check if there is type information for this item
        try:
            name_type = markdown[: markdown.index(": ") + 2]
            ntr = re.search(
                r"(\(((\*\*Required\*\*)|(\*Optional\*))(,\s(.*))*)\):\s",
                name_type,
                re.IGNORECASE,
            )
            if ntr:
                param_type = ntr.group(6)
                if param_type:
                    markdown = (
                        f"**{param_type}**: {markdown[markdown.index(': ') + 2 :]}"
                    )
        except ValueError:
            # ': ' not found
            pass

        title = list(node.traverse(nodes.title))[0]
        if len(title) > 0:
            url = urllib.parse.urljoin(
                self.app.config.html_baseurl,
                self.docname + ".html#" + title.parent["ids"][0],
            )
            markdown += f"\n\n*See also: [{self.props_section_title}]({url})*"
        return markdown

    def update_prop(self, node, props):
        prop_name = None

        raw = node.rawsource  # this has the full raw rst code for this property

        if not raw.startswith("**"):
            # not bolded, most likely not a property definition,
            # usually texts like 'All properties from...' etc
            return None

        markdown = self.getMarkdown(node)

        markdown += f"\n\n*See also: [{self.props_section_title}]({urllib.parse.urljoin(self.app.config.html_baseurl, self.docname +'.html#'+self.title_id)})*"

        try:
            name_type = markdown[: markdown.index(": ") + 2]
        except ValueError:
            raise ValueError(f'Property format error. Missing ": " in {raw}')

        # Example properties formats are:
        # **name** (**Required**, string): Long Description...
        # **name** (*Optional*, string): Long Description... Defaults to ``value``.
        # **name** (*Optional*): Long Description... Defaults to ``value``.

        ntr = re.search(
            r"\* \*\*(\w*)\*\*\s(\(((\*\*Required\*\*)|(\*Optional\*))(,\s(.*))*)\):\s",
            name_type,
            re.IGNORECASE,
        )

        if ntr:
            prop_name = ntr.group(1)
            param_type = ntr.group(7)
        else:
            s2 = re.search(
                r"\* \*\*(\w*)\*\*\s(\(((\*\*Required\*\*)|(\*Optional\*))(,\s(.*))*)\):\s",
                markdown,
                re.IGNORECASE,
            )
            if s2:
                # this is e.g. when a property has a list inside, and the list inside are the options.
                # just validate **prop_name**
                s3 = re.search(r"\* \*\*(\w*)\*\*:\s", name_type)
                prop_name = s3.group(1)
                param_type = None
            else:
                raise ValueError(f"Invalid property format: {node.rawsource}")

        k = str(prop_name)
        jprop = props.get(k)
        if not jprop:
            # Create docs for common properties when descriptions are overriden
            # in the most specific component.

            if k in [
                "id",
                "name",
                "internal",
                # i2c
                "address",
                "i2c_id",
                # polling component
                "update_interval",
                # uart
                "uart_id",
                # ligth
                "effects",
                "gamma_correct",
                "default_transition_length",
                "color_correct",
                # display
                "lambda",
                "dither",
                "pages",
                "rotation",
                # spi
                "spi_id",
                "cs_pin",
                # output (binary/float output)
                "inverted",
                "power_supply",
                # climate
                "receiver_id",
            ]:
                jprop = props[k] = {}
            else:
                raise ValueError(f"Cannot find property {k}")

        desc = markdown[markdown.index(": ") + 2 :].strip()
        if param_type:
            desc = "**" + param_type + "**: " + desc

        jprop["markdownDescription"] = desc
        global props_documented
        props_documented = props_documented + 1

        return prop_name

    def get_ref(self, node):
        ref = node.get("$ref")
        if ref and ref.startswith("#/definitions/"):
            return self.app.jschema["definitions"][ref[14:]]

    def find_component(self, component_path):
        path = component_path.split("/")
        if path[0] not in ("properties", "definitions"):
            return None
        json_component = self.app.jschema[path[0]][path[1]]

        if len(path) > 2:
            # a property path
            props = self.find_props(json_component)
            if props:
                json_component = props.get(path[2])
            else:
                # a platform sub element
                json_component = find_platform_component(
                    self.app.jschema, path[1], path[2]
                )
        return json_component

    class Props(MutableMapping):
        """Smarter props dict.

        Props are mostly a dict, however some constructs have two issues:
        - An update is intended on an element which does not own a property, but it is based
        on an schema that does have the property, those cases can be handled
        - An update is done in a typed schema
        """

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
                arr = component.get("anyOf", component.get("allOf"))
                if not arr:
                    if "$ref" in component:
                        return self._get_props(self.visitor.get_ref(component))
                    return None
                for x in arr:
                    props = x.get("properties")
                    if not ref:
                        ref = self.visitor.get_ref(x)
                    if props:
                        break
            if not props and ref:
                props = self._get_props(ref)
            return props

        def __getitem__(self, key):
            if self.store and key in self.store:
                return self.store[key]

            if "then" in self.component:
                # check if it's typed
                schemas = self.component["then"].get("allOf")
                if (
                    isinstance(schemas, list)
                    and "properties" in schemas[0]
                    and "type" in schemas[0]["properties"]
                ):
                    for s in schemas:
                        if "then" in s:
                            props = self._get_props(s.get("then"))
                            if key in props:
                                return SetObservable(
                                    props[key],
                                    setitem_callback=self._update_typed,
                                    inner_key=key,
                                )
                    return  # key not found

                # check if it's a registry and need to reset store
                # e.g. remote_receiver binary sensor
                if "$ref" in self.component["then"]:
                    ref = self.visitor.get_ref(self.component["then"])
                    prop_set = ref.get("anyOf")
                    if isinstance(prop_set, list):
                        for k in prop_set:
                            if "$ref" in k:
                                k = self.visitor.get_ref(k)
                            if key in k["properties"]:
                                self.store = k["properties"]
                                return self.store[key]

        def _update_typed(self, inner_key, key, value):
            # Make sure we update all types
            if "then" in self.component:
                schemas = self.component["then"].get("allOf")
                assert "type" in schemas[0].get("properties")
                for s in schemas:
                    if "then" in s:
                        props = self._get_props(s.get("then"))
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


def handle_component(app, doctree, docname):
    path = docname.split("/")
    if path[0] == "components":
        pass
    elif docname not in CUSTOM_DOCS:
        return

    v = SchemaGeneratorVisitor(app, doctree, docname)
    doctree.walkabout(v)


def build_finished(app, exception):
    # TODO: create report of missing descriptions

    f = open(SCHEMA_PATH, "w")
    f.write(json.dumps(app.jschema))

    str = f"Documented: {props_documented}"
    logger = logging.getLogger(__name__)
    logger.info(str)


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
