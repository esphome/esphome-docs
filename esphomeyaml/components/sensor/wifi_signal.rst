WiFi Signal Sensor
==================

The ``wifi_signal`` sensor platform allows you to read the signal
strength of the currently connected WiFi Access Point.

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: wifi_signal
        name: "WiFi Signal Sensor"
        update_interval: 15s

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **name** (**Required**, string): The name of the hall effect sensor.
- **update_interval** (*Optional*, :ref:`config-time`): The interval
  to check the sensor. Defaults to ``15s``. See :ref:`sensor-default_filter`.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

.. warning::

    Signal strength readings are only available when WiFi in in station mode. Readings are not valid
    if the device is acting as an access point without any station mode connection.

See Also
^^^^^^^^

- :ref:`sensor-filters`
- :doc:`adc`
- :doc:`API Reference </api/sensor/adc-sensor>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/wifi_signal.rst>`__
