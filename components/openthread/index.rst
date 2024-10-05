OpenThread Component
=====================

.. seo::
    :description: Instructions for setting up OpenThread component that represent their state as a string of text.
    :image: folder-open.svg

Text sensors are a lot like normal :doc:`sensors </components/sensor/index>`.
But where the "normal" sensors only represent sensors that output **numbers**, this
component can represent any *text*.

.. _config-text_sensor:

Base Text Sensor Configuration
------------------------------

.. code-block:: yaml

    # Example sensor configuration
    name: Livingroom Temperature

    # Optional variables:
    icon: "mdi:water-percent"

Configuration variables:

- **id** (*Optional*, string): Manually specify the ID for code generation. At least one of **id** and **name** must be specified.
- **name** (*Optional*, string): The name for the sensor. At least one of **id** and **name** must be specified.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the text sensor to use that name, you can set ``name: None``.

- **icon** (*Optional*, icon): Manually set the icon to use for the sensor in the frontend.
- **device_class** (*Optional*, string): The device class for the
  sensor. Only the ``timestamp`` and ``date`` device classes are supported.
  Set to ``""`` to remove the default device class of a sensor.
  Requires Home Assistant 2024.3 or newer.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options.
  Set to ``""`` to remove the default entity category.
- If MQTT enabled, All other options from :ref:`MQTT Component <config-mqtt-component>`.
- If Webserver enabled, ``web_server_sorting_weight`` can be set. See :ref:`Webserver Entity Sorting <config-webserver-sorting>`.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`text_sensor-on_value`.
- **on_raw_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is received that hasn't passed through any filters. See :ref:`text_sensor-on_raw_value`.

.. _text_sensor-filters:

Text Sensor Filters
-------------------

ESPHome allows you to do some basic pre-processing of
text_sensor values before they’re sent to Home Assistant. This is for example
useful if you want to manipulate the text_sensor string in some fashion.

There are a lot of filters that sensors support. You define them by adding a ``filters``
block in the text_sensor configuration (at the same level as ``platform``; or inside each text_sensor block
for platforms with multiple sensors).

Filters are processed in the order they are defined in your configuration.

.. code-block:: yaml

    # Example filters:
    filters:
      - to_upper:
      - to_lower:
      - append: "_suffix"
      - prepend: "prefix_"
      - substitute:
        - "suf -> foo"
        - "pre -> bar"
      - lambda: return {"Hello World"};
