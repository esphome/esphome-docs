APC Smart UPS
=============

.. seo::
    :description: Instructions for setting up APC UPS compatible with Smart protocol.

The ``apcups`` component allows you to integrate an APC UPS compatible with Smart 
protocol in ESPHome. It uses :ref:`UART <uart>` for communication.

Once configured you can use sensors as described below for your projects.

Overview
--------

Most APC UPSes have a male DB9 connector on their back allowing for monitoring and control 
via the SmartUPS protocol. This connector is not wired as a standard serial port, pinout 
corresponds to APC's factory cable ``940-024C``. Also, since this port works at standard
RS232 (``5V``) levels, it cannot be connected directly to the MCU. A level shifter module 
has to be used like this one:

.. figure:: ../images/smart-ups_hw-027.jpg
    :align: center

    HW-027 level shifter module connections to a smart-compatible UPS

APC UPSes communicate at ``2400`` baud (older models) or ``9200`` baud (newer models).

Component
---------

A configured UART is required.

.. code-block:: yaml

    # Example configuration entry
    uart:
        id: ups
        rx_pin: GPIO3
        tx_pin: GPIO1
        baud_rate: 2400

    sensor:
      - platform: apcups
        id: myups
        internal_temp:
          id: temp
          name: Internal Temperature
        battery_voltage:
          id: bat
          name: Battery Voltage
        battery_level:
          id: batlev
          name: Battery level
        power_load:
          id: load
          name: Power load
        input_voltage:
          id: inv
          name: Input Voltage
        output_voltage:
          id: ouv
          name: Output Voltage
        line_frequency:
          id: freq
          name: Line Frequency
        estimated_runtime:
          id: runt
          name: Estimated Runtime


Configuration variables:

- **ph**: Measured pH value
- **temperature**: Measured temperature value
- **dis1**: Measured DIS 1 value
- **dis2**: Measured DIS 2 value
- **redox**: Measured Redox value
- **ec**: Measured EC value
- **oci**: Measured OCI value


All sensors are *Optional* and support all other options from :ref:`Sensor <config-sensor>`.

.. note::

    If you are using an ESP8266, serial logging may cause problems reading from UART. For best 
    results, hardware serial is recommended. Software serial may not be able to read all 
    received data if other components spend a lot of time in the ``loop()``.

    For hardware serial only a limited set of pins can be used. Either ``tx_pin: GPIO1`` and 
    ``rx_pin: GPIO3``  or ``tx_pin: GPIO15`` and ``rx_pin: GPIO13``.

    The disadvantage of using the hardware uart is that you can't use serial logging because 
    the serial logs would be sent to the modbus device and cause errors.

    Serial logging can be disabled by setting ``baud_rate: 0``.

    See :doc:`logger` for more details

    .. code-block:: yaml

        logger:
            level: <level>
            baud_rate: 0


See Also
--------

- :ref:`uart`
- :doc:`logger`
- :ref:`Sensor <config-sensor>`
- `UPS Constants <https://kirbah.github.io/apc-ups/UPS-constants/>`__
- `APC smart protocol <http://www.apcupsd.org/manual/manual.html#apc-smart-protocol>`__
- :ghedit:`Edit`
