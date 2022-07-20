Input Text Component
================

.. seo::
    :description: Instructions for setting up input text components in ESPHome.
    :image: folder-open.svg

ESPHome has support for components to create an input text entity. An input text entity is
like a sensor that can read a value from a device, but is useful when that value
can be set by the user/frontend.

.. _config-input_text:

Base Input Text Configuration
-------------------------

All input texts in ESPHome have a name and an optional icon.

.. code-block:: yaml

    # Example input text configuration
    name: Greeting

    # Optional variables:
    icon: "mdi:text"
    entity_category: config

Configuration variables:

- **name** (**Required**, string): The name for the input text.
- **icon** (*Optional*, icon): Manually set the icon to use for the input text in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Requires Home Assistant 2021.11 or newer.
  Set to ``""`` to remove the default entity category.
- **mode** (*Optional*, string): Defines how the input text should be displayed in the frontend.
  Can either be ``auto``, ``string`` or ``password``.
  Defaults to ``"auto"``.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`input_text-on_value`.

MQTT Options:

- All other options from :ref:`MQTT Component <config-mqtt-component>`.

Input Text Automation
-----------------

You can access the most recent state of the input text in :ref:`lambdas <config-lambda>` using
``id(input_text_id).state``.

.. _input_text-on_value:

``on_value``
************

This automation will be triggered when a new value is published. In :ref:`Lambdas <config-lambda>`
you can get the value from the trigger with ``x``.

.. code-block:: yaml

    input_text:
      - platform: template
        # ...
        on_value:
          then:
            - light.turn_on:
                id: light_1
                red: !lambda "return x/255;"

Configuration variables: See :ref:`Automation <automation>`.

.. _input_text-set_action:

``input_text.set`` Action
*********************

This is an :ref:`Action <config-action>` for setting a input text state.

.. code-block:: yaml

    - input_text.set:
        id: my_text
        value: "Good bye!"

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the input text to set.
- **value** (**Required**, string, :ref:`templatable <config-templatable>`):
  The value to set the input text to.



See Also
--------

- :apiref:`Input Text <input_text/input_text.h>`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
