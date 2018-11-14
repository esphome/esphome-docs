Text Sensor Component
=====================

.. seo::
    :description: Instructions for setting up text sensors that represent their state as a string of text.
    :image: folder-open.svg

Text sensors are a lot like normal :doc:`sensors </esphomeyaml/components/sensor/index>`.
But where the "normal" sensors only represent sensors that output **numbers**, this
component can represent any *text*.

.. _config-text_sensor:

Base Text Sensor Configuration
------------------------------

.. code:: yaml

    # Example sensor configuration
    name: Livingroom Temperature

    # Optional variables:
    icon: "mdi:water-percent"

Configuration variables:

- **name** (**Required**, string): The name for the sensor.
- **icon** (*Optional*, icon): Manually set the icon to use for the sensor in the frontend.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`text_sensor-on_value`.

Text Sensor Automation
----------------------

You can access the most recent state of the sensor in :ref:`lambdas <config-lambda>` using
``id(sensor_id).value``.

.. _text_sensor-on_value:

``on_value``
************

This automation will be triggered when a new value is published.
In :ref:`Lambdas <config-lambda>` you can get the value from the trigger with ``x``.

.. code:: yaml

    text_sensor:
      - platform: version
        # ...
        on_value:
          then:
            - lambda: |-
                ESP_LOGD("main", "The current version is %s", x.c_str());

Configuration variables: See :ref:`Automation <automation>`.

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all text sensors to do some
advanced stuff (see the full :doc:`API Reference </api/sensor/index>` for more info).

- ``publish_state()``: Manually cause the sensor to push out a value.

  .. code:: yaml

      // Within lambda, push a value of "Hello World"
      id(my_sensor).publish_state("Hello World");

- ``.state``: Retrieve the current value of the sensor as an ``std::string`` object.

  .. code:: yaml

      // For example, create a custom log message when a value is received:
      std::string val = id(my_sensor).state;
      ESP_LOGI("main", "Value of my sensor: %s", val.c_str());

See Also
--------

- :doc:`API Reference </api/text_sensor/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/text_sensor/index.rst>`__

.. toctree::
    :maxdepth: 1

    version
    mqtt_subscribe
    template

.. disqus::
