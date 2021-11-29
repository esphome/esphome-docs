Button Component
================

.. seo::
    :description: Instructions for setting up button components in ESPHome.
    :image: folder-open.svg

ESPHome has support for components to create a button entity. A button entity is
basically a momentary switch with no state and can be triggered by either yaml or
the user/frontend.

.. note::

    Home Assistant Core 2021.12 or higher is required for ESPHome button entities to work.

.. _config-button:

Base Button Configuration
-------------------------

All buttons in ESPHome have a name and an optional icon.

.. code-block:: yaml

    # Example button configuration
    name: Livingroom Lazy Mood
    id: my_button

    # Optional variables:
    icon: "mdi:emoticon-outline"

Configuration variables:

- **name** (**Required**, string): The name for the button.
- **icon** (*Optional*, icon): Manually set the icon to use for the button in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Set to ``""`` to remove the default entity category.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`select-on_value`.

MQTT Options:

- All other options from :ref:`MQTT Component <config-mqtt-component>`.

Button Automation
-----------------

.. _button-on_press:

``on_press``
************

This automation will be triggered when the button is pressed.

.. code-block:: yaml

    button:
      - platform: template
        # ...
        on_press:
          then:
            - logger.log: Button Pressed

Configuration variables: See :ref:`Automation <automation>`.

.. _button-press_action:

``button.press`` Action
***********************

This is an :ref:`Action <config-action>` for pressing a button in an Automation.

.. code-block:: yaml

    - button.press: my_button

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.

.. _button-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can press a button.

- ``press()``: Set the select option.

  .. code-block:: cpp

      // Within lambda, press the button.
      id(my_button).press();

See Also
--------

- :apiref:`button/button.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
