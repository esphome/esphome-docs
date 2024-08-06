Modem Sensor
============

.. seo::
    :description: Fetch numeric values from Modem.

The ``modem`` platform is a sensor platform that can
query  :doc:`/components/modem` for specific values of service characteristics.

.. note::

    The :doc:`/components/modem` must have ``enable_cmux`` set to **True**.


.. code-block:: yaml

    modem:
      id: atmodem
      rx_pin: GPIO26
      tx_pin: GPIO27
      status_pin: GPIO34
      model: SIM7600
      apn: orange
      enable_cmux: True

    sensor:
    - platform: modem
      rssi:
        name: rssi
      ber:
        name: ber
      latitude:
        name: Latitude
      longitude:
        name: Longitude
      altitude:
        name: Altitude
        

Configuration variables:
------------------------

- **rssi** (*Optional*): Received Signal Strength Indicator, in dB. From -113 dB (lowest), to -51 (highest). All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **ber** (*Optional*): Bit Error Rate, in %. May not be available on all modem models. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **latitude** (*Optional*): GNSS latitude in degrees. Require ``enable_gnss: True`` in :doc:`/components/modem`. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **longitude** (*Optional*): GNSS longitude in degrees. Require ``enable_gnss: True`` in :doc:`/components/modem`. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **altitude** (*Optional*): GNSS altitude, in meters. Require ``enable_gnss: True`` in :doc:`/components/modem`. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to poll the device. Defaults to ``60s``.
- All other options from :ref:`Text Sensor <config-text_sensor>`.


See Also
--------

- :doc:`/components/modem`
- :doc:`/components/text_sensor/modem`
- :ref:`sensor-filters`
- :ghedit:`Edit`
