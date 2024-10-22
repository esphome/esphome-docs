UART Switch
===========

.. seo::
    :description: Instructions for setting up UART switches in ESPHome that can output arbitrary UART sequences when activated.
    :image: uart.svg

The ``uart`` switch platform allows you to send a pre-defined sequence of bytes on a
:doc:`UART bus </components/uart>` when triggered.

.. code-block:: yaml

    # Example configuration entry
    switch:
      - platform: uart
        name: "UART String Output"
        data: 'DataToSend'
      - platform: uart
        name: "UART Bytes Output"
        data: [0xDE, 0xAD, 0xBE, 0xEF]
      - platform: uart
        name: "UART Recurring Output"
        data: [0xDE, 0xAD, 0xBE, 0xEF]
        send_every: 1s
      - platform: uart
        name: "UART On/Off"
        data:
          turn_on: "TurnOn\r\n"
          turn_off: "TurnOff\r\n"

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the UART hub.
- **data** (*Optional*, string or list of bytes): The data to send via UART. Either an ASCII string
  or a list of bytes or one or both of the following nested options (see example above).

  - **turn_on** (*Optional*, string or list of bytes): The data to send when turning on.
  - **turn_off** (*Optional*, string or list of bytes): The data to send when turning off.
- **send_every** (*Optional*, :ref:`config-time`): Sends recurring data instead of sending once.
- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`/components/uart`
- :apiref:`uart/switch/uart_switch.h`
- :ghedit:`Edit`
