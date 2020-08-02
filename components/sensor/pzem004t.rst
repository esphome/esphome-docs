Peacefair PZEM-004T Energy Monitor
==================================

.. seo::
    :description: Instructions for setting up PZEM-004T power monitors.
    :image: pzem004t.png
    :keywords: PZEM-004T

.. note::

    This page is incomplete and could some work. If you want to contribute, please read the
    :doc:`contributing guide </guides/contributing>`. This page is missing:

      - An image for the front page.
      - Images/screenshots/example configs of this device being used in action.

The ``pzem004t`` sensor platform allows you to use PZEM-004T energy monitors
(`website <https://innovatorsguru.com/ac-digital-multifunction-meter-using-pzem-004t/>`__) sensors with
ESPHome.

.. warning::

    This page refers to version V1 of the PZEM004T, which has been out of stock for a while.
    For using the newer V3 variant of this sensor please see :doc:`pzemac <pzemac>`.

The communication with this integration is done over a :ref:`UART bus <uart>`.
You must therefore have a ``uart:`` entry in your configuration with both the TX and RX pins set
to some pins on your board and the baud rate set to 9600.

.. code-block:: yaml

    # Example configuration entry
    uart:
      tx_pin: D1
      rx_pin: D2
      baud_rate: 9600

    sensor:
      - platform: pzem004t
        current:
          name: "PZEM-004T Current"
        voltage:
          name: "PZEM-004T Voltage"
        power:
          name: "PZEM-004T Power"
        energy:
          name: "PZEM-004T Energy"
        update_interval: 60s

Configuration variables:
------------------------

- **current** (*Optional*): Use the current value of the sensor in amperes. All options from
  :ref:`Sensor <config-sensor>`.
- **power** (*Optional*): Use the (active) power value of the sensor in watts. All options from
  :ref:`Sensor <config-sensor>`.
- **voltage** (*Optional*): Use the voltage value of the sensor in volts.
  All options from :ref:`Sensor <config-sensor>`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

See Also
--------

- :ref:`sensor-filters`
- :doc:`pzemac`
- :doc:`pzemdc`
- :apiref:`pzem004t/pzem004t.h`
- :ghedit:`Edit`
