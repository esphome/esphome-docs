WiFi Signal Sensor
==================

.. seo::
    :description: Instructions for setting up WiFi signal sensors that track the RSSI connection strength value to the network.
    :image: network-wifi.png

The ``wifi_signal`` sensor platform allows you to read the signal
strength of the currently connected :doc:`WiFi Access Point </components/wifi>`.

The sensor value is the `"Received signal strength indication" <https://en.wikipedia.org/wiki/Received_signal_strength_indication>`__
measured in decibels. These values are always negative and the closer they are to zero, the better the signal is.

.. figure:: images/wifi_signal-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: wifi_signal
        name: "WiFi Signal Sensor"
        update_interval: 60s

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the WiFi signal sensor.
- **update_interval** (*Optional*, :ref:`config-time`): The interval
  to check the sensor. Defaults to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

.. warning::

    Signal strength readings are only available when WiFi is in station mode. Readings are not valid
    if the device is acting as an access point without any station mode connection.

Example: Converting dB to %
---------------------------

The conversion from dB to % isn't well-defined (see disussion `"here" <https://www.adriangranados.com/blog/dbm-to-percent-conversion>`__) but the Arduino wire library and Tasmota both use this formula: RSSI_Percent = min(max(2 * (RSSI + 100.0), 0.0), 100.0) (that is, add 100 and multiply by 2, then cap at 100% max and 0% min), which truncates any dB lower than -100 or higher than -50. The ESP8266 goes as low as -120 and high as +4 in my experiance, but the very low and high values don't add much real information.

.. code-block:: yaml

    filters:
      - lambda: return min(max(2 * (x + 100.0), 0.0), 100.0);
    unit_of_measurement: "%"


See Also
--------

- :ref:`sensor-filters`
- :doc:`/components/wifi`
- :apiref:`wifi_signal/wifi_signal_sensor.h`
- :ghedit:`Edit`
