Jablotron Component
===================

.. seo::
    :description: Instructions for setting up Jablotron in ESPHome.
    :keywords: Jablotron

The `jablotron` component configures a RS-485 connection to a Jablotron 
JA-121T gateway using the :doc:`UART bus </components/uart>`.

.. code-block:: yaml

    uart:
      tx_bin: GPIO1
      rx_pin: GPIO3
      baud_rate: 9600

    jablotron:
      flow_control_pin: GPIO15

    binary_sensor:
      - platform: jablotron_peripheral
        index: 1
        name: "Entryway motion"
        device_class: motion
      - platform: jablotron_section_flag
        index: 1
        flag: ENTRY
        name: "Alarm entry delay"

    text_sensor:
      - platform: jablotron_info
        name: "Jablotron Info"
      - platform: jablotron_section
        index: 1
        name: Alarm


Configuration variables:
------------------------

- **access_code** (*Optional*, string): The access code to use for authenticated actions
  (e.g. arming a section or setting a PG). Individual components can override this.

- **flow_control_pin** (*Optional*, :ref:`config-pin`): The pin used to switch flow control.
  This is useful for RS485 transceivers that do not have automatic flow control switching,
  like the common MAX485.

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>`
  if you want to use multiple UART buses.

See Also
---------

- :apiclass:`:jablotron::JablotronComponent`
- :doc:`/components/binary_sensor/jablotron_peripheral`
- :doc:`/components/binary_sensor/jablotron_section_flag`
- :doc:`/components/text_sensor/jablotron_info`
- :doc:`/components/text_sensor/jablotron_section`
- :doc:`/components/uart`
- `JA-121 RS-485 Interface <https://jablotron.com.hk/image/data/pdf/manuel/JA-121T.pdf>`__
- :ghedit:`Edit`
