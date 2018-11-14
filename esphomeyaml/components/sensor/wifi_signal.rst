WiFi Signal Sensor
==================

.. seo::
    :description: Instructions for setting up WiFi signal sensors that track the RSSI connection strength value to the network.
    :image: network-wifi.svg

The ``wifi_signal`` sensor platform allows you to read the signal
strength of the currently connected :doc:`WiFi Access Point </esphomeyaml/components/wifi>`.

The sensor value is the `"Received signal strength indication" <https://en.wikipedia.org/wiki/Received_signal_strength_indication>`__
measured in decibels. These values are always negative and the closer they are to zero, the better the signal is.

.. figure:: images/wifi_signal-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: wifi_signal
        name: "WiFi Signal Sensor"
        update_interval: 15s

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the hall effect sensor.
- **update_interval** (*Optional*, :ref:`config-time`): The interval
  to check the sensor. Defaults to ``15s``. See :ref:`sensor-default_filter`.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

.. warning::

    Signal strength readings are only available when WiFi is in station mode. Readings are not valid
    if the device is acting as an access point without any station mode connection.

See Also
--------

- :ref:`sensor-filters`
- :doc:`/esphomeyaml/components/wifi`
- :doc:`API Reference </api/sensor/wifi_signal>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/wifi_signal.rst>`__

.. disqus::
