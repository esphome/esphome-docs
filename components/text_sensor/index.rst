Text Sensor Component
=====================

.. seo::
    :description: Instructions for setting up text sensors that represent their state as a string of text.
    :image: folder-open.png

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

- **name** (**Required**, string): The name for the sensor.
- **icon** (*Optional*, icon): Manually set the icon to use for the sensor in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.
- If MQTT enabled, All other options from :ref:`MQTT Component <config-mqtt-component>`.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`text_sensor-on_value`.

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
