UART Switch
===========

.. seo::
    :description: Instructions for setting up UART switches in esphomelib that can output arbitrary UART sequences when activated.
    :image: uart.svg

The ``uart`` switch platform allows you to send a pre-defined sequence of bytes on a
:doc:`UART bus </esphomeyaml/components/uart>` when triggered.

.. code:: yaml

    # Example configuration entry
    uart:
      baud_rate: 9600
      tx_pin: D0

    switch:
      - platform: uart
        name: "UART String Output"
        data: 'DataToSend'
      - platform: uart
        name: "UART Bytes Output"
        data: [0xDE, 0xAD, 0xBE, 0xEF]

Configuration variables:
------------------------

- **data** (**Required**, string or list of bytes): The data to send via UART. Either an ASCII string
  or a list of bytes.
- **name** (**Required**, string): The name for the switch.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the UART hub.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`/esphomeyaml/components/uart`
- :doc:`API Reference </api/switch/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/uart.rst>`__

.. disqus::
