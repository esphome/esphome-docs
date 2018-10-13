Status Binary Sensor
====================

The Status Binary Sensor exposes the node state (if it’s connected to
MQTT or not) for Home Assistant. It uses the :ref:`MQTT birth and last will messages <mqtt-last_will_birth>`
to do this.

.. figure:: images/status-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: status
        name: "Living Room Status"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`
  and :ref:`MQTT Component <config-mqtt-component>`. (Inverted mode is not supported)

See Also
--------

- :doc:`/esphomeyaml/components/binary_sensor/index`
- :doc:`/esphomeyaml/components/mqtt`
- :doc:`API Reference </api/binary_sensor/status>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/status.rst>`__

.. disqus::
