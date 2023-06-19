SUN_GTIL2 Grid Tie Inverter
===========================

.. seo::
    :description: Instructions for reading data from a SUN-1000G2 grid tie inverter using ESPHome
    :keywords: sun-1000g2, sun-2000g2, sun1000, sun2000, sun-1000gtil2, sun-2000gtil2

The ``sun_gtil2`` component allows you to get voltage, power and temperature readings from your ``SUN-1000G2``
or ``SUN-2000G2`` grid tie inverter. This is done by reading the UART data transmitted from the inverter's
controller board to the display board.

.. note::

    You need to open your inverter to apply this modification. Use at your own risk! If you want to connect your
    inverter via the (more limited) external RS232 interface you should use the
    :doc:`Modbus </components/modbus_controller>` component instead.

As the data is read from the inverter using UART, you need to have an :ref:`UART bus <uart>` in your
configuration with the ``rx_pin`` connected to the TX pin of the inverter's controller board. Additionally, you
need to set the ``baud_rate`` to 9600.

.. code-block:: yaml

    # Example configuration entry
    uart:
      - id: control_to_display
        rx_pin: GPIO16
        baud_rate: 9600

    sun_gtil2:
      uart_id: control_to_display
      temperature:
        id: gtil_temperature
        name: "Heatsink Temperature"
        filters:
          - throttle_average: 30s
      dc_voltage:
        id: gtil_dc_voltage
        name: "DC Voltage"
        filters:
          - throttle_average: 30s
      ac_voltage:
        id: gtil_ac_voltage
        name: "AC Voltage"
        filters:
          - throttle_average: 30s
      dc_power:
        id: gtil_dc_power
        name: "DC Power"
      ac_power:
        id: gtil_ac_power
        name: "AC Power"
      state:
        id: gtil_state
        name: "State"
      limiter_power:
        id: gtil_limiter_power
        internal: True
      serial_number:
        id: gtil_serial_number
        internal: True

The inverter will report new measurements approximately every 1.3 seconds.

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

- **temperature** (*Optional*): The temperature of your inverter's heatsink.
  All options from :ref:`Sensor <config-sensor>`.

- **dc_voltage** (*Optional*): The voltage of your DC source. (battery or solar panels)
  All options from :ref:`Sensor <config-sensor>`.

- **ac_voltage** (*Optional*): The grid voltage measured by the inverter.
  All options from :ref:`Sensor <config-sensor>`.

- **dc_power** (*Optional*): The inverter's input power.
  All options from :ref:`Sensor <config-sensor>`.

- **ac_power** (*Optional*): The inverter's output power.
  All options from :ref:`Sensor <config-sensor>`.

- **limiter_power** (*Optional*): The power measured by the inverter's "Internal" limiter.
  All options from :ref:`Sensor <config-sensor>`.

- **state** (*Optional*): The inverter's state.
  All options from :ref:`Text Sensor <config-text_sensor>`.

- **serial_number** (*Optional*): The inverter's serial number.
  All options from :ref:`Text Sensor <config-text_sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :ghedit:`Edit`
