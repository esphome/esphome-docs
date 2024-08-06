Modem Text Sensor
=================

.. seo::
    :description: Fetch string values from Modem.

The ``modem`` platform is a text sensor platform that can
query  :doc:`/components/modem` for specific values of service characteristics.

.. note::

    The :doc:`/components/modem` must have ``enable_cmux`` set to **True**.


.. code-block:: yaml

    modem:
      id: atmodem
      model: SIM7600
      enable_cmux: True
      apn: orange

    text_sensor:
      - platform: modem
        network_type:
          name: network type
        update_interval: 10s
        

Configuration variables:
------------------------

- **network_type** (*Optional*): Expose the modem network type (GSM, GPRS, LTE...) as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to poll the device. Defaults to ``60s``.
- All other options from :ref:`Text Sensor <config-text_sensor>`.


See Also
--------

- :doc:`/components/modem`
- :doc:`/components/sensor/modem`
- :ref:`sensor-filters`
- :ghedit:`Edit`
