Text Sensor Component
=====================

.. seo::
    :description: Instructions for setting up text sensors that represent their state as a string of text.
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
- If Webserver enabled and version 3 is selected, All other options from Webserver Component.. See :ref:`Webserver Version 3 <config-webserver-version-3-options>`.

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

``to_upper``
************

Converts all characters within a string to uppercase (only the English alphabet is supported at this time).

.. code-block:: yaml

    # Example configuration entry
    - platform: template
      # ...
      filters:
        - to_upper:

``to_lower``
************

Converts all characters within a string to lowercase (only the English alphabet is supported at this time).

.. code-block:: yaml

    # Example configuration entry
    - platform: template
      # ...
      filters:
        - to_lower:

``append``
**********

Adds a string to the end of the current string.

.. code-block:: yaml

    # Example configuration entry
    - platform: template
      # ...
      filters:
        - append: "_suffix"

``prepend``
***********

Adds a string to the start of the current string.

.. code-block:: yaml

    # Example configuration entry
    - platform: template
      # ...
      filters:
        - prepend: "prefix_"

``substitute``
**************

Search the current value of the text sensor for a string, and replace it with another string.

.. code-block:: yaml

    # Example configuration entry
    - platform: template
      # ...
      filters:
        - substitute:
          - "suf -> foo"
          - "pre -> bar"

The arguments are a list of substitutions, each in the form ``TO_FIND -> REPLACEMENT``.

``map``
*******

Lookup the current value of the text sensor in a list, and return the matching item if found.
Does not change the value of the text sensor if the current value wasn't found.


.. code-block:: yaml

    # Example configuration entry
    - platform: template
      # ...
      filters:
        - map:
          - high -> On
          - low -> Off

The arguments are a list of substitutions, each in the form ``LOOKUP -> REPLACEMENT``.

``lambda``
**********

Perform a advanced operations on the text sensor value. The input string is ``x`` and
the result of the lambda is used as the output (use ``return``).

.. code-block:: yaml

    filters:
      - lambda: |-
          if (x == "Hello") {
            return x + "bar";
          } else {
            return x + "foo";
          }

Text Sensor Automation
----------------------

You can access the most recent state of the sensor in :ref:`lambdas <config-lambda>` using
``id(sensor_id).state``.

.. _text_sensor-on_value:

``on_value``
************

This automation will be triggered when a new value is published.
In :ref:`Lambdas <config-lambda>` you can get the value from the trigger with ``x``.

.. code-block:: yaml

    text_sensor:
      - platform: version
        # ...
        on_value:
          then:
            - lambda: |-
                ESP_LOGD("main", "The current version is %s", x.c_str());

Configuration variables: See :ref:`Automation <automation>`.

.. _text_sensor-on_raw_value:

``on_raw_value``
****************

This automation will be triggered when a new value is received that hasn't passed
through any filters. In :ref:`Lambdas <config-lambda>` you can get the value from the trigger with ``x``.

.. code-block:: yaml

    text_sensor:
      - platform: version
        # ...
        on_raw_value:
          then:
            - lambda: |-
                ESP_LOGD("main", "The current version is %s", x.c_str());

Configuration variables: See :ref:`Automation <automation>`.

.. _text_sensor-state_condition:

``text_sensor.state`` Condition
-------------------------------

This :ref:`Condition <config-condition>` allows you to check if a given text sensor
has a specific state.

.. code-block:: yaml

    on_...:
      - if:
          condition:
            # Checks if "my_text_sensor" has state "Hello World"
            text_sensor.state:
              id: my_text_sensor
              state: 'Hello World'

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The text sensor ID.
- **state** (**Required**, :ref:`templatable <config-templatable>`, string): The state to compare
  to.

.. note::

    This condition can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        if (id(my_text_sensor).state == "Hello World") {
          // do something
        }

.. _text_sensor-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all text sensors to do some
advanced stuff (see the full API Reference for more info).

- ``publish_state()``: Manually cause the sensor to push out a value.

  .. code-block:: cpp

      // Within lambda, push a value of "Hello World"
      id(my_sensor).publish_state("Hello World");

- ``.state``: Retrieve the current value of the sensor as an ``std::string`` object.

  .. code-block:: cpp

      // For example, create a custom log message when a value is received:
      std::string val = id(my_sensor).state;
      ESP_LOGI("main", "Value of my sensor: %s", val.c_str());

See Also
--------

- :apiref:`text_sensor/text_sensor.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
