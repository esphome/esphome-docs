GPIO Binary Sensor
==================

The GPIO Binary Sensor platform allows you to use any input pin on your
device as a binary sensor.

.. figure:: images/gpio-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: gpio
        pin: D2
        name: "Living Room Window"
        device_class: window

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to periodically check.
- **name** (**Required**, string): The name of the binary sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`
  and :ref:`MQTT Component <config-mqtt-component>`.

See Also
^^^^^^^^

- :doc:`/esphomeyaml/components/binary_sensor/index`
- :ref:`config-pin_schema`
- :doc:`API Reference </api/binary_sensor/gpio>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/gpio.rst>`__
