Button Component
================

.. seo::
    :description: Instructions for setting up button components in ESPHome.
    :image: folder-open.svg

.. note::

    To attach a physical button to ESPHome, see
    :doc:`GPIO Binary Sensor </components/binary_sensor/gpio>`.

ESPHome has support for components to create button entities in Home Assistant. A button entity is
represented in ESPHome as a momentary switch with no state and can be triggered in Home Assistant
via the UI or automations.

.. note::

    Home Assistant Core 2021.12 or higher is required for ESPHome button entities to work.

.. _config-button:

Base Button Configuration
-------------------------

All buttons in ESPHome have a name and an optional icon.

.. code-block:: yaml

    # Example button configuration
    button:
      - platform: ...
        name: Livingroom Lazy Mood
        id: my_button

        # Optional variables:
        icon: "mdi:emoticon-outline"
        on_press:
          - logger.log: "Button pressed"

Configuration variables:

- **id** (*Optional*, string): Manually specify the ID for code generation. At least one of **id** and **name** must be specified.
- **name** (*Optional*, string): The name for the button. At least one of **id** and **name** must be specified.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the button to use that name, you can set ``name: None``.

- **icon** (*Optional*, icon): Manually set the icon to use for the button in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Set to ``""`` to remove the default entity category.
- **device_class** (*Optional*, string): The device class for the button.
  See https://www.home-assistant.io/integrations/button/#device-class
  for a list of available options.
- If Webserver enabled and version 3 is selected, All other options from Webserver Component.. See :ref:`Webserver Version 3 <config-webserver-version-3-options>`.

Automations:

- **on_press** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the button is pressed. See :ref:`button-on_press`.

MQTT options:

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

Configuration variables: see :ref:`Automation <automation>`.

.. _button-press_action:

``button.press`` Action
***********************

This is an :ref:`Action <config-action>` for pressing a button in an Automation.

.. code-block:: yaml

    - button.press: my_button

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the button to set.

.. note::

    Buttons are designed to trigger an action on a device from Home Assistant, and have an unidirectional flow from
    Home Assistant to ESPHome. If you press a button using this action, no button press event will be triggered in Home
    Assistant. If you want to trigger an automation in Home Assistant, you should use a
    :ref:`Home Assistant event <api-homeassistant_event_action>` instead.

.. _button-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can press a button.

- ``press()``: Press the button.

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
