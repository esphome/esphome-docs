"""
ESPHome Sphinx Extension.

This extension provides ESPHome documentation specific.  While it may be a good starting
point for other projects, the esoteric nature of the included code is designed to assist
in automating the linking and indexing of components, devices, and blueprints.

Because Sphinx internals are foreign to most people looking through this, the documentation
in this file will verbose.  (Future me thanks you for leaving them here too.)

Quick and dirty usage guide:

* Component support:
  * Definition: `.. esphome::component-definition::`
  * Reference: `:esphome:component:`component-category:component-alias``
  * Index: `.. esphome:index:: Components`
* Device support:
  * Definition: `.. esphome::device-definition::`
  * Reference: `:esphome:device:`device-category:device-alias``
  * Index: `.. esphome:index:: Devices`
* Cookbook support:
  * Definition: `.. esphome::cookbook-entry::`
  * Reference: `:esphome:recipe:`ble-itag``
  * Index: `.. esphome:index:: Cookbook`

Further notes:

* `sphinx.addnodes.pending_xref` doesn't quite solve the problem due to domain data;
* TOC image parsing is limited to things in /images/<name>.
"""

from sphinx.transforms import SphinxContentsFilter

from os import path
import os
from docutils.parsers.rst.states import Inliner
from docutils.parsers.rst import Directive, directives
from docutils.nodes import Element, Node, system_message
from docutils import nodes, utils
from multiprocessing.sharedctypes import Value
from itertools import zip_longest
from sphinx.domains import Domain
from sphinx.environment.adapters.toctree import TocTree
from sphinx.roles import XRefRole
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.nodes import make_refnode
from sphinx.util import logging
from sphinx import addnodes
from typing import (TYPE_CHECKING, Dict, List, Tuple, Type, TypeVar, cast)

N = TypeVar('N')


if TYPE_CHECKING:
    from sphinx.environment import BuildEnvironment
    from sphinx.builders import Builder
    from sphinx.config import Config


# Enable proper logging instead of just using print all the time.
logger = logging.getLogger(__name__)

"""
Constants are defined here to keep things cleaner internally.
The aim is to remove the potential for mistakes in copying.
"""

# Common
_ESPHOME_DOMAIN = 'esphome'  # .. <domain>:
_INDEX_DIRECTIVE = 'index'  # Index directive (common)
_ALIAS_KEY = 'alias'
_DOCNAME_KEY = 'docname'
_DISPNAME_KEY = 'dispname'
_DESCRIPTOR_KEY = 'descriptor'  # Descriptor
_TOC_KEY = 'toc'
_DOMAIN_KEY = 'domain'
_CATEGORY_KEY = 'category'
_SECTION_KEY = 'section'
_FRIENDLY_NAME = 'friendly_name'  # Friendly name
_TOC_GROUP = 'toc_group'  # Table of Contents group.
_TOC_IMAGE = 'toc_image'  # Table of Contents image

# Configuration/Env work used by this extension.
_ENV_CONFIGURATION_KEY = 'esphome'

# Component related
_COMPONENT_DIRECTIVE_DEFINE = 'component-definition'
_COMPONENT_DIRECTIVE = 'component'
_COMPONENT_KEY = 'component'
_COMPONENTS_KEY = 'components'  # Storage category
_COMPONENTS_TOC_KEY = 'components_toc'  # Storage category

# Device related
_DEVICE_DIRECTIVE_DEFINE = 'device-definition'
_DEVICE_DIRECTIVE = 'device'
_DEVICE_KEY = 'device'  # Storage category
_DEVICE_TOC_KEY = 'device_toc'  # Storage category

# Cookbook related
_COOKBOOK_KEY = 'cookbook'  # Storage key
_COOKBOOK_DIRECTIVE_DEFINE = 'cookbook-entry'
_COOKBOOK_DIRECTIVE = 'recipe'
_COOKBOOK_DEVICES = 'devices'
_COOKBOOK_COMPONENTS = 'components'
_COOKBOOK_TABLE_KEY = 'Cookbook'

_RECIPE_DEVICES_HEADING = 'Devices used in this Recipe'
_RECIPE_COMPONENTS_HEADING = 'Components used in this Recipe'

# Dummy element for fast searching.


class esphome_node(nodes.Inline, nodes.TextElement):
    pass


def visit_esphome_node(self, node):
    pass


def depart_esphome_node(self, node):
    pass


def _image_table_generator(env, docname, builder, cols, data_key, category_key):
    """Single category table generator."""
    # Domain (usually 'esphome')
    domain = env.get_domain(_ESPHOME_DOMAIN)

    # For this to work it uses a {cat: {name: obj}} structure.
    data_parent = domain.data[data_key]
    data = []
    if category_key == None:
        data = data_parent  # Cookbook
    else:
        if category_key not in data_parent:
            return []
        data = data_parent[category_key]
    data_keys = list(data.keys())
    data_keys.sort()

    items = []
    for key in data_keys:
        row = data[key]
        name = row[_FRIENDLY_NAME]
        page = row[_DOCNAME_KEY]
        image = row[_TOC_IMAGE]
        item = {
            "name": name.strip(),
            "link": builder.get_relative_uri(docname, page),
            "image": "/images/{}".format(image),
        }
        if _DESCRIPTOR_KEY in row:
            item["category"] = row[_DESCRIPTOR_KEY]
        else:
            item["category"] = ""
        items.append(item)

    table = nodes.table()
    table["classes"].append("table-center")
    table["classes"].append("colwidths-given")

    # Set up column specifications based on widths
    tgroup = nodes.tgroup(cols=cols)
    table += tgroup
    tgroup.extend(nodes.colspec(colwidth=1) for _ in range(cols))

    tbody = nodes.tbody()
    tgroup += tbody
    rows = []
    for value in zip_longest(fillvalue=None, *([iter(items)] * cols)):
        trow = nodes.row()
        for cell in value:
            entry = nodes.entry()
            if cell is None:
                entry += nodes.paragraph()
                trow += entry
                continue
            name = cell["name"]
            link = cell["link"]
            image = cell["image"]
            reference_node = nodes.reference(refuri=link)
            img = nodes.image(uri=directives.uri(image), alt=name)
            img["classes"].append("component-image")
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
            name = cell["name"]
            link = cell["link"]
            ref = nodes.reference(name, name, refuri=link)
            para = nodes.paragraph()
            para += ref
            entry += para
            cat_text = cell["category"]
            if cat_text:
                cat = nodes.paragraph(text=cat_text)
                entry += cat
            trow += entry
        rows.append(trow)
    tbody.extend(rows)

    return [table]


_TABLE_TYPES = {
    'Devices': {
        _DOMAIN_KEY: _ESPHOME_DOMAIN,
        _TOC_KEY: _DEVICE_TOC_KEY,
        _CATEGORY_KEY: _CATEGORY_KEY,
        _SECTION_KEY: 'devices',
    },
    'Components': {
        _DOMAIN_KEY: _ESPHOME_DOMAIN,
        _TOC_KEY: _COMPONENTS_TOC_KEY,
        _CATEGORY_KEY: _CATEGORY_KEY,
        _SECTION_KEY: 'components',
    },
    _COOKBOOK_TABLE_KEY: {
        _DOMAIN_KEY: _ESPHOME_DOMAIN,
        _TOC_KEY: _COOKBOOK_KEY,
        _SECTION_KEY: 'cookbook'
    }
}


class IndexTableDirective(SphinxDirective):
    has_content = True
    required_arguments = 1
    option_spec = {
        # Columns
        "columns": directives.positive_int,
        # Friendly name is required
        _TOC_GROUP: directives.unchanged,
    }

    def run(self):
        arg0 = self.arguments[0]
        if arg0 not in _TABLE_TYPES:
            raise AttributeError("IndexTableDirective requires a type.")
        cols = self.options.get("columns", 3)
        toc_group = ''
        attributes = {
            'esphome': 'image_table',
            'table_type': arg0,
            'columns': cols,
        }
        if _TOC_GROUP in self.options:
            toc_group = self.options.get(_TOC_GROUP, '')
            if toc_group != '':
                attributes['toc_group'] = toc_group
        targetnode = esphome_node('', **attributes)
        return [targetnode]


def _common_role_worker(category, instance, subdomain, domain=_ESPHOME_DOMAIN):
    attributes = {
        'esphome': 'role',
        'subdomain': subdomain,
        'category': category,
        'instance': instance,
    }
    targetnode = esphome_node('', **attributes)
    return [targetnode], []


class ComponentRole(SphinxRole):
    """A custom role for enabling cross-reference work for ESPHome components."""
    # Sphinx doesn't provide env or state to SphinxRole.

    def __call__(self, name: str, rawtext: str, text: str, lineno: int,
                 inliner: Inliner, options: Dict = {}, content: List[str] = []
                 ) -> Tuple[List[Node], List[system_message]]:
        fragments = text.split(":")  # category, target
        if len(fragments) == 2:
            return _common_role_worker(fragments[0], fragments[1], _COMPONENT_KEY, _ESPHOME_DOMAIN)
        else:
            raise ValueError("fragment length should be exactly 2")


class DeviceRole(SphinxRole):
    """A custom role for enabling cross-reference work for ESPHome devices."""

    def __call__(self, name: str, rawtext: str, text: str, lineno: int,
                 inliner: Inliner, options: Dict = {}, content: List[str] = []
                 ) -> Tuple[List[Node], List[system_message]]:
        fragments = text.split(":")  # category, target
        if len(fragments) == 2:
            return _common_role_worker(fragments[0], fragments[1], _DEVICE_KEY, _ESPHOME_DOMAIN)
        else:
            raise ValueError("fragment length should be exactly 2")


class CookbookRole(SphinxRole):
    """A custom role for enabling cross-reference work for ESPHome recipes/cookbook entries."""

    def __call__(self, name: str, rawtext: str, text: str, lineno: int,
                 inliner: Inliner, options: Dict = {}, content: List[str] = []
                 ) -> Tuple[List[Node], List[system_message]]:
        # Nothing remotely special, just the name of the recipe.
        return _common_role_worker('', text.strip().rstrip(), _COOKBOOK_KEY, _ESPHOME_DOMAIN)


class CookbookDefinitionDirective(Directive):
    """A custom directive for handling cookbook/recipe additions.

    By way of example:

    ```rst
    .. esphome:cookbook-entry::
      :alias: ble-itag
      :friendly_name: ESP32 BLE iTag Button
      :toc_image: esp32_ble_itag.jpg
      :devices: espressif:esp32
      :components: core:ble-client,sensor:ble-client
    ```

    This should be put at the bottom of the page, below `See Also`.
    It will turn into a list containing devices and components links.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        # Aliasing key
        _ALIAS_KEY: directives.unchanged_required,
        # Display name
        _FRIENDLY_NAME: directives.unchanged_required,
        # List group (programmatic alias) - optional here
        _TOC_GROUP: directives.unchanged,
        # Image for TOC
        _TOC_IMAGE: directives.unchanged_required,
        # Optional comma separated list of devices in the form of:
        # <device_category>:<device_alias>
        _COOKBOOK_DEVICES: directives.unchanged,
        # Optional comma separated list of components in the form of:
        # <component_category>:<component_alias>
        _COOKBOOK_COMPONENTS: directives.unchanged,
    }

    def run(self):
        if _ALIAS_KEY in self.options\
           and _FRIENDLY_NAME in self.options\
           and _TOC_IMAGE in self.options:
            # Alias is used for attributes
            alias = self.options.get(_ALIAS_KEY).strip().rstrip()
            # Get the ESPHome domain.
            esphome = self.state.document.settings.env.get_domain(_ESPHOME_DOMAIN)
            devices_raw = self.options.get(_COOKBOOK_DEVICES, '')
            devices = []
            if devices_raw != '':
                for device in devices_raw.split(','):
                    devices.append(device.strip().rstrip())
            components_raw = self.options.get(_COOKBOOK_COMPONENTS, '')
            components = []
            if components_raw != '':
                for component in components_raw.split(','):
                    components.append(component.strip().rstrip())
            # TOC Group is used for attributes
            toc_group = self.options.get(_TOC_GROUP, '').strip().rstrip()
            # Add the component (paranoid strip and rstrip)
            esphome.add_cookbook_recipe(alias,
                                        self.options.get(_FRIENDLY_NAME).strip().rstrip(),
                                        toc_group,
                                        self.options.get(_TOC_IMAGE).strip().rstrip(),
                                        devices,
                                        components
                                        )
            # Store an entry for replacement.
            attributes = {
                'esphome': 'cookbook',
                'category': toc_group,
                'instance': alias,
            }
            return [esphome_node('', **attributes)]
        else:
            return []


class ComponentDefinitionDirective(Directive):
    """A custom directive for handling component addition.

    This directive is within the `esphome` domain.

    By way of example:

    ```rst
    .. esphome:component-definition::
      :alias: analog_threshold
      :category: binary_sensor
      :friendly_name: Analog Threshold
      :toc_group: Binary Sensor
      :toc_image: analog_threshold.svg
      :descriptor: optional 'category' field
    ```

    For the purposes of multiple listings, category and toc_group,
    may contain multiple values split on semi-colons (`;`).
    `category` must be either one value or equal to toc_group.

    The optional descriptor is shared amongst all toc_groups.

    The TOC group is the 'pretty' name.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        # Aliasing key
        _ALIAS_KEY: directives.unchanged_required,
        # Type (subdirectory/path)
        _CATEGORY_KEY: directives.unchanged_required,
        # Display name
        _FRIENDLY_NAME: directives.unchanged_required,
        # List group (programmatic alias)
        _TOC_GROUP: directives.unchanged_required,
        # Image for TOC
        _TOC_IMAGE: directives.unchanged_required,
        # Descriptor ('category' under the old system)
        # e.g. 'Temperature'
        _DESCRIPTOR_KEY: directives.unchanged,
    }

    def run(self):
        if _ALIAS_KEY in self.options\
           and _CATEGORY_KEY in self.options\
           and _FRIENDLY_NAME in self.options\
           and _TOC_GROUP in self.options\
           and _TOC_IMAGE in self.options:
            # Get the ESPHome domain.
            esphome = self.state.document.settings.env.get_domain(_ESPHOME_DOMAIN)

            alias = self.options.get(_ALIAS_KEY).strip().rstrip()
            category = self.options.get(_CATEGORY_KEY).strip().rstrip()
            friendly_name = self.options.get(_FRIENDLY_NAME).strip().rstrip()
            toc_group = self.options.get(_TOC_GROUP).strip().rstrip()
            toc_image = self.options.get(_TOC_IMAGE).strip().rstrip()
            descriptor = self.options.get(_DESCRIPTOR_KEY, '').strip().rstrip()

            if toc_group.count(';') > 0:
                categories = category.split(';')
                toc_groups = toc_group.split(';')
                if len(categories) == 1:
                    for i in range(len(toc_groups)):
                        esphome.add_component(alias,
                                              category,
                                              friendly_name,
                                              toc_groups[i].strip().rstrip(),
                                              toc_image,
                                              descriptor)
                elif len(categories) == len(toc_groups):
                    for i in range(len(toc_groups)):
                        esphome.add_component(alias,
                                              categories[i].strip().rstrip(),
                                              friendly_name,
                                              toc_groups[i].strip().rstrip(),
                                              toc_image,
                                              descriptor)

                else:
                    raise ValueError("categories must either be one value or equal to toc_groups")
            else:
                esphome.add_component(alias,
                                      category,
                                      friendly_name,
                                      toc_group,
                                      toc_image,
                                      descriptor)
        return []


class DeviceDefinitionDirective(Directive):
    """A custom component for handling device addition.

    This directive is within the `esphome` domain.

    By way of example:

    ```rst
    .. esphome:device-definition::
      :alias: esp32
      :category: espressif
      :friendly_name: Generic ESP32
      :toc_group: Espressif
      :toc_image: esp32.svg
    ```

    The TOC group is the 'pretty' name.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        # Aliasing key
        _ALIAS_KEY: directives.unchanged_required,
        # Type (subdirectory/path)
        _CATEGORY_KEY: directives.unchanged_required,
        # Display name
        _FRIENDLY_NAME: directives.unchanged_required,
        # List group (programmatic alias)
        _TOC_GROUP: directives.unchanged_required,
        # Image for TOC
        _TOC_IMAGE: directives.unchanged_required,
        # Descriptor ('category' under the old system)
        # e.g. 'Temperature'
        _DESCRIPTOR_KEY: directives.unchanged,
    }

    def run(self):
        if _ALIAS_KEY in self.options\
                and _CATEGORY_KEY in self.options\
                and _FRIENDLY_NAME in self.options\
                and _TOC_GROUP in self.options\
                and _TOC_IMAGE in self.options:
            # Get the ESPHome domain.
            esphome = self.state.document.settings.env.get_domain(_ESPHOME_DOMAIN)
            # Add the component (paranoid strip and rstrip)
            esphome.add_device(self.options.get(_ALIAS_KEY).strip().rstrip(),
                               self.options.get(_CATEGORY_KEY).strip().rstrip(),
                               self.options.get(_FRIENDLY_NAME).strip().rstrip(),
                               self.options.get(_TOC_GROUP).strip().rstrip(),
                               self.options.get(_TOC_IMAGE).strip().rstrip(),
                               self.options.get(_DESCRIPTOR_KEY, '').strip().rstrip(),
                               )
        return []


class ESPHomeDomain(Domain):
    """A custom domain to handle ESPHome documentation needs."""
    name = _ESPHOME_DOMAIN
    label = 'ESPHome Component'
    roles = {
        'ref': XRefRole(),
        _COMPONENT_DIRECTIVE: ComponentRole(),
        _DEVICE_DIRECTIVE: DeviceRole(),
        _COOKBOOK_DIRECTIVE: CookbookRole(),
    }
    directives = {
        _COMPONENT_DIRECTIVE_DEFINE: ComponentDefinitionDirective,
        _COOKBOOK_DIRECTIVE_DEFINE: CookbookDefinitionDirective,
        _DEVICE_DIRECTIVE_DEFINE: DeviceDefinitionDirective,
        _INDEX_DIRECTIVE: IndexTableDirective,
    }
    indices = {}

    initial_data = {
        # Components: category -> {name -> object}
        _COMPONENTS_KEY: {},  # Useful for subpage filtration.

        # Components: toc-category -> {name -> object}
        _COMPONENTS_TOC_KEY: {},

        # Devices: device_path -> {name -> object}
        _DEVICE_KEY: {},  # Useful for subpage filtration.

        # Devices: device_path -> {name -> object}
        _DEVICE_TOC_KEY: {},

        # Cookbook: recipe -> information.
        _COOKBOOK_KEY: {},
    }

    def get_full_qualified_name(self, node):
        """Gets the path to the internally registered type.

        This needs to be validated if the system is expanded.
        """
        return '{}.{}'.format(_ESPHOME_DOMAIN, node.arguments[0])

    def get_objects(self):
        """Required for search functionality, so must yield appropriately or it all breaks."""
        components_by_category = self.data[_COMPONENTS_KEY]
        for category_key in components_by_category:
            components = components_by_category[category_key]
            component_keys = list(components.keys())
            component_keys.sort()
            for component_key in component_keys:
                component = components[component_key]
                # fullname, dispname, type, docname, anchor, prio
                yield((
                    component[_ALIAS_KEY],  # fullname
                    component[_DISPNAME_KEY],  # dispname
                    _COMPONENT_KEY,  # type
                    component[_DOCNAME_KEY],  # docname
                    component[_ALIAS_KEY].replace("_", "-").replace(" ", "-"),  # anchor
                    0,  # priority of 0
                ))

        devices_by_type = self.data[_DEVICE_KEY]
        for category_key in devices_by_type:
            devices = devices_by_type[category_key]
            device_keys = list(devices.keys())
            device_keys.sort()
            for device_key in device_keys:
                device = devices[device_key]
                # fullname, dispname, type, docname, anchor, prio
                yield((
                    device[_ALIAS_KEY],  # fullname
                    device[_DISPNAME_KEY],  # dispname
                    _DEVICE_KEY,  # type
                    device[_DOCNAME_KEY],  # docname
                    device[_ALIAS_KEY].replace("_", "-").replace(" ", "-"),  # anchor
                    0,  # priority of 0
                ))

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        match = [(docname, anchor)
                 for name, sig, typ, docname, anchor, prio
                 in self.get_objects() if sig == target]

        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]

            return make_refnode(builder, fromdocname, todocname, targ,
                                contnode, targ)
        else:
            return None

    def add_component(self, alias, component_type, friendly_name, toc_group, toc_image, descriptor):
        """Add a component to the domain."""

        # Build the component.
        component = {
            _DISPNAME_KEY: '{}.{}'.format('component', alias),
            _ALIAS_KEY: alias,
            _CATEGORY_KEY: component_type,
            _FRIENDLY_NAME: friendly_name,
            _TOC_GROUP: toc_group,
            _TOC_IMAGE: toc_image,
            _DOCNAME_KEY: self.env.docname,
            _DESCRIPTOR_KEY: descriptor,
        }

        # Store the component using default information.
        if component_type not in self.data[_COMPONENTS_KEY]:
            self.data[_COMPONENTS_KEY][component_type] = {}
        self.data[_COMPONENTS_KEY][component_type][alias] = component

        # Store the component in the toc_group.
        if toc_group not in self.data[_COMPONENTS_TOC_KEY]:
            self.data[_COMPONENTS_TOC_KEY][toc_group] = {}
        self.data[_COMPONENTS_TOC_KEY][toc_group][alias] = component

    def add_device(self, alias, category, friendly_name, toc_group, toc_image, descriptor):
        """Add a device to the domain."""

        # Build the device.
        device = {
            _DISPNAME_KEY: '{}.{}'.format('device', alias),
            _ALIAS_KEY: alias,
            _CATEGORY_KEY: category,
            _FRIENDLY_NAME: friendly_name,
            _TOC_GROUP: toc_group,
            _TOC_IMAGE: toc_image,
            _DOCNAME_KEY: self.env.docname,
            _DESCRIPTOR_KEY: descriptor,
        }

        # Store the component using default information.
        if category not in self.data[_DEVICE_KEY]:
            self.data[_DEVICE_KEY][category] = {}
        self.data[_DEVICE_KEY][category][alias] = device

        # Store the component in the toc_group.
        if toc_group not in self.data[_DEVICE_TOC_KEY]:
            self.data[_DEVICE_TOC_KEY][toc_group] = {}
        self.data[_DEVICE_TOC_KEY][toc_group][alias] = device

        # TODO: Store by board type and/or chipset?

    def add_cookbook_recipe(self, alias, friendly_name, toc_group, toc_image, devices, components):
        recipe = {
            _DISPNAME_KEY: '{}.{}'.format('recipe', alias),
            _ALIAS_KEY: alias,
            _FRIENDLY_NAME: friendly_name,
            _TOC_GROUP: toc_group,
            _TOC_IMAGE: toc_image,
            _COOKBOOK_DEVICES: devices,
            _DOCNAME_KEY: self.env.docname,
            _COOKBOOK_COMPONENTS: components,
        }
        self.data[_COOKBOOK_KEY][alias] = recipe

        # TODO: Attempt back-reference to devices/components?


def _image_post_process(app, doctree, fromdocname):
    """Follow the pattern of the image collector to avoid hacking things up too far.
    Remember to add images to the environment before using this or nothing will work.
    """

    # Find all images
    for node in doctree.findall(nodes.image):
        # mimetype = image
        # * forces selection (skip)
        # ? is for non-local (skip)
        candidates: Dict[str, str] = {}
        node['candidates'] = candidates
        imguri = node['uri']
        if imguri.startswith('data:'):
            candidates['?'] = imguri
            continue
        elif imguri.find('://') != -1:
            candidates['?'] = imguri
            continue

        # Get relative form.
        node['uri'], _ = app.env.relfn2path(imguri, fromdocname)
        candidates['*'] = node['uri']

        # Ensure unique name.
        for imgpath in candidates.values():
            app.env.dependencies[fromdocname].add(imgpath)
            if not os.access(path.join(app.srcdir, imgpath), os.R_OK):
                logger.warning('image file not readable: %s' % imgpath,
                               location=node, type='image', subtype='not_readable')
                continue
            app.env.images.add_file(fromdocname, imgpath)


def _on_doctree_resolved(app, doctree, fromdocname):
    """Activates when the doctree-resolved event/signal is raised.

    This is where pending esphome-sphinx nodes are updated against the final doctree.
    """

    env = app.builder.env
    requires_image_update = False
    requires_toc_update = False
    domain = env.get_domain(_ESPHOME_DOMAIN)

    # Prevent a fault downstream if this is empty.
    if not hasattr(env, _ENV_CONFIGURATION_KEY):
        setattr(env, _ENV_CONFIGURATION_KEY, [])

    # Replace all esphome_node instances.
    for node in doctree.findall(esphome_node):
        attributes = node.attributes
        if 'esphome' in attributes:
            requires_toc_update = True
            if attributes['esphome'] == 'role':
                if attributes['subdomain'] == _COOKBOOK_KEY:
                    try:
                        data_collection = domain.data[attributes['subdomain']]
                        data_instance = data_collection[attributes['instance']]
                        print(data_instance)
                        title = data_instance[_FRIENDLY_NAME]
                        target = app.builder.get_relative_uri(fromdocname, data_instance[_DOCNAME_KEY])
                        reference_node = nodes.reference(title, utils.unescape(title), refuri=target, **{})
                        node.replace_self(reference_node)
                    except KeyError as e:
                        logger.warning('esphome role node missing key: %s' % e,
                                       location=node, type='esphome-role', subtype='keyerror')
                        node.replace_self([])
                else:
                    try:
                        data_collection = domain.data[attributes['subdomain']]
                        data_category = data_collection[attributes['category']]
                        data_instance = data_category[attributes['instance']]
                        title = data_instance[_FRIENDLY_NAME]
                        target = app.builder.get_relative_uri(fromdocname, data_instance[_DOCNAME_KEY])
                        reference_node = nodes.reference(title, utils.unescape(title), refuri=target, **{})
                        node.replace_self(reference_node)
                    except KeyError as e:
                        logger.warning('esphome role node missing key: %s' % e,
                                       location=node, type='esphome-role', subtype='keyerror')
                        node.replace_self([])
            elif attributes['esphome'] == 'cookbook':
                # Cookbook listing.
                replacements = []
                # Cookbook
                cookbook = domain.data[_COOKBOOK_KEY]
                # Get components
                # `nodes.list_item` is not an instance of nodes.TextElement, so it will throw
                # an error if you remove the nodes.line() (which is the safest TextElement to use).
                if attributes['instance'] in cookbook:
                    recipe = cookbook[attributes['instance']]
                    if len(recipe[_COOKBOOK_DEVICES]) > 0:
                        recipe_devices = []
                        for device in recipe[_COOKBOOK_DEVICES]:
                            fragments = device.split(":")
                            if len(fragments) == 2:
                                if fragments[0] in domain.data[_DEVICE_KEY]:
                                    category = domain.data[_DEVICE_KEY][fragments[0]]
                                    if fragments[1] in category:
                                        recipe_devices.append(category[fragments[1]])
                        if len(recipe_devices) > 0:
                            section = nodes.section(ids=['cookbook-definition-devices'])
                            section += nodes.title(_RECIPE_DEVICES_HEADING, _RECIPE_DEVICES_HEADING)
                            list_object = nodes.bullet_list()
                            for device in recipe_devices:
                                target = app.builder.get_relative_uri(fromdocname, device[_DOCNAME_KEY])
                                text = nodes.line()
                                text += nodes.reference(device[_FRIENDLY_NAME], utils.unescape(device[_FRIENDLY_NAME]), refuri=target, **{})
                                list_item = nodes.list_item()
                                list_item += text
                                list_object += list_item
                            section += list_object
                            replacements.append(section)
                    if len(recipe[_COOKBOOK_COMPONENTS]) > 0:
                        recipe_components = []
                        for component in recipe[_COOKBOOK_COMPONENTS]:
                            fragments = component.split(":")
                            if len(fragments) == 2:
                                if fragments[0] in domain.data[_COMPONENTS_KEY]:
                                    category = domain.data[_COMPONENTS_KEY][fragments[0]]
                                    if fragments[1] in category:
                                        recipe_components.append(category[fragments[1]])
                        if len(recipe_components) > 0:
                            section = nodes.section(ids=['cookbook-definition-components'])
                            section += nodes.title(_RECIPE_COMPONENTS_HEADING, _RECIPE_COMPONENTS_HEADING)
                            list_object = nodes.bullet_list()
                            for component in recipe_components:
                                target = app.builder.get_relative_uri(fromdocname, component[_DOCNAME_KEY])
                                text = nodes.line()
                                text += nodes.reference(component[_FRIENDLY_NAME], utils.unescape(component[_FRIENDLY_NAME]), refuri=target, **{})
                                list_item = nodes.list_item()
                                list_item += text
                                list_object += list_item
                            section += list_object
                            replacements.append(section)
                node.replace_self(replacements)
            elif attributes['esphome'] == 'image_table':
                requires_image_update = True
                if attributes['table_type'] == _COOKBOOK_TABLE_KEY:
                    table_type = _TABLE_TYPES[attributes['table_type']]
                    data_key = table_type[_TOC_KEY]  # TOC key
                    node.replace_self(
                        _image_table_generator(env,
                                               fromdocname,
                                               app.builder,
                                               attributes['columns'],
                                               data_key,
                                               None)
                    )
                else:
                    if 'toc_group' in attributes:
                        table_type = _TABLE_TYPES[attributes['table_type']]
                        data_key = table_type[_TOC_KEY]  # TOC key
                        node.replace_self(
                            _image_table_generator(env,
                                                   fromdocname,
                                                   app.builder,
                                                   attributes['columns'],
                                                   data_key,
                                                   attributes['toc_group'])
                        )
                    else:
                        replacements = []
                        table_type = _TABLE_TYPES[attributes['table_type']]
                        data_key = table_type[_TOC_KEY]  # TOC key
                        toc_groups = list(domain.data[data_key].keys())
                        toc_groups.sort()
                        for toc_group in toc_groups:
                            # toc group is not anchor-safe, fix this
                            anchor_friendly_id = '{}-{}'.format(
                                table_type[_SECTION_KEY],
                                toc_group
                            ).lower().replace(' ', '-').replace('_', '-').strip().rstrip()  # paranoia
                            section = nodes.section(ids=[anchor_friendly_id])  # Create a container.
                            section += nodes.title(toc_group, toc_group)
                            section += _image_table_generator(env,
                                                              fromdocname,
                                                              app.builder,
                                                              attributes['columns'],
                                                              data_key,
                                                              toc_group)
                            replacements.append(section)
                        node.replace_self(replacements)
            else:
                # Shouldn't be here.
                node.replace_self([])

    if requires_image_update:
        # If any image work is done, we neded to fix it.  This isn't ideal.
        _image_post_process(app, doctree, fromdocname)
    if requires_toc_update:
        # Only slightly tweaked from the Sphinx source:
        # sphinx/environment/collectors/toctree.py#L52
        numentries = [0]

        def traverse_in_section(node: Element, cls: Type[N]) -> List[N]:
            """Like traverse(), but stay within the same section."""
            result: List[N] = []
            if isinstance(node, cls):
                result.append(node)
            for child in node.children:
                if isinstance(child, nodes.section):
                    continue
                elif isinstance(child, nodes.Element):
                    result.extend(traverse_in_section(child, cls))
            return result

        def build_toc(node: Element, depth: int = 1) -> nodes.bullet_list:
            entries: List[Element] = []
            for sectionnode in node:
                if isinstance(sectionnode, nodes.section):
                    title = sectionnode[0]
                    visitor = SphinxContentsFilter(doctree)
                    title.walkabout(visitor)
                    nodetext = visitor.get_entry_text()
                    if not numentries[0]:
                        anchorname = ''
                    else:
                        anchorname = '#' + sectionnode['ids'][0]
                    numentries[0] += 1
                    reference = nodes.reference(
                        '', '', internal=True, refuri=fromdocname,
                        anchorname=anchorname, *nodetext)
                    para = addnodes.compact_paragraph('', '', reference)
                    item: Element = nodes.list_item('', para)
                    sub_item = build_toc(sectionnode, depth + 1)
                    if sub_item:
                        item += sub_item
                    entries.append(item)
                elif isinstance(sectionnode, addnodes.only):
                    onlynode = addnodes.only(expr=sectionnode['expr'])
                    blist = build_toc(sectionnode, depth)
                    if blist:
                        onlynode += blist.children
                        entries.append(onlynode)
                elif isinstance(sectionnode, nodes.Element):
                    for toctreenode in traverse_in_section(sectionnode,
                                                           addnodes.toctree):
                        item = toctreenode.copy()
                        entries.append(item)
                        TocTree(app.env).note(fromdocname, toctreenode)
            if entries:
                return nodes.bullet_list('', *entries)
            return None
        toc = build_toc(doctree)
        if toc:
            app.env.tocs[fromdocname] = toc
        else:
            app.env.tocs[fromdocname] = nodes.bullet_list('')
        app.env.toc_num_entries[fromdocname] = numentries[0]


def setup(app):
    # Creates/installs the domain for directives and roles.
    app.add_domain(ESPHomeDomain)

    app.add_node(esphome_node,
                 html=(visit_esphome_node, depart_esphome_node),
                 latex=(visit_esphome_node, depart_esphome_node),
                 text=(visit_esphome_node, depart_esphome_node))

    # Document tree is resolved: now safe to update the stubs.
    # https://www.sphinx-doc.org/en/master/extdev/appapi.html#event-doctree-resolved
    app.connect('doctree-resolved', _on_doctree_resolved)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
