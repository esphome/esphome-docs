MQTT Subscribe Text Sensor
==========================

.. seo::
    :description: Instructions for setting up MQTT Subscribe text sensors that show the content of a MQTT message as their state.
    :image: mqtt.png
    :keywords: MQTT

The ``mqtt_subscribe`` text sensor platform allows you to get external data into esphomelib.
The sensor will subscribe to messages on the given MQTT topic and save the most recent value
in its ``id(mysensor).value``.

.. code:: yaml

    # Example configuration entry
    text_sensor:
      - platform: mqtt_subscribe
        name: "Data from topic"
        id: mysensor
        topic: the/topic

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the text sensor.
- **topic** (**Required**, string): The MQTT topic to listen for numeric messages.
- **qos** (*Optional*, int): The MQTT QoS to subscribe with. Defaults to ``0``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Text Sensor <config-text_sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

Example Usage for Displays
--------------------------

This integration is especially useful for displays, to show external data on the display.
Please note you have to use the ``.c_str()`` method on the ``.state`` object together with the ``%s`` format
to use it in ``printf`` expressions.

.. code:: yaml

    # Example configuration entry
    text_sensor:
      - platform: mqtt_subscribe
        name: "Data from topic"
        id: mysensor
        topic: the/topic

    display:
      - platform: ...
        # ...
        lambda: |-
          it.printf(0, 0, id(font), "The data is: %s", id(mysensor).state.c_str());

See Also
--------

- :doc:`API Reference </api/text_sensor/mqtt_subscribe>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/text_sensor/mqtt_subscribe.rst>`__

.. disqus::
