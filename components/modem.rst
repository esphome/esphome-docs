Modem Component
===============

.. seo::
    :description: Instructions for setting up the Modem configuration for your ESP32 node in ESPHome.
    :image: modem.svg
    :keywords: Modem, ESP32

This ESPHome component enables *cellular* modem connections for ESP32s.

This component and the Wi-Fi component may **not** be used simultaneously, even if both are physically available.

.. code-block:: yaml

    # Example configuration entry for a modem
    modem:
      type: SIM800
      tx_pin: GPIOXX
      rx_pin: GPIOXX
      reset_pin: GPIOXX
      power_pin: GPIOXX
      pwrkey_pin: GPIOXX
      apn: "internet"
      uart_event_task_stack_size: 2048
      uart_event_task_priority: 5
      uart_event_queue_size: 30
      tx_buffer_size: 512
      rx_buffer_size: 1024

Configuration variables:
------------------------

- **type** (**Required**, string): The type of modem.

  Supported modems are:

  - ``BG96``
  - ``SIM800``
  - ``SIM7000``
  - ``SIM7070``

- **tx_pin** (**Required**, :ref:`config-pin`): The TX pin of the modem.
- **rx_pin** (**Required**, :ref:`config-pin`): The RX pin of the modem.
- **reset_pin** (*Optional*, :ref:`config-pin`): The reset pin of the modem.
- **power_pin** (*Optional*, :ref:`config-pin`): The power pin of the modem.
- **pwrkey_pin** (*Optional*, :ref:`config-pin`): The power key pin of the modem.
- **apn** (*Optional*, string): The Access Point Name (APN) for the modem. Default is "internet".
- **uart_event_task_stack_size** (*Optional*, int): The stack size for the UART event task. Default is 2048.
- **uart_event_task_priority** (*Optional*, int): The priority for the UART event task. Default is 5.
- **uart_event_queue_size** (*Optional*, int): The size of the UART event queue. Default is 30.
- **tx_buffer_size** (*Optional*, int): The size of the TX buffer. Default is 512.
- **rx_buffer_size** (*Optional*, int): The size of the RX buffer. Default is 1024.
- **use_address** (*Optional*, string): Manually override what address to use to connect to the ESP. Defaults to auto-generated value.
- **domain** (*Optional*, string): Set the domain of the node hostname used for uploading. Defaults to ``.local``.

.. note::

    The modem component requires at least a reset pin, a power pin, or a pwrkey pin to be configured.

Configuration examples
----------------------

**Example configuration for a SIM800 modem**:

.. code-block:: yaml

    modem:
      type: SIM800
      tx_pin: GPIO17
      rx_pin: GPIO16
      reset_pin: GPIO5
      power_pin: GPIO4
      pwrkey_pin: GPIO0
      apn: "internet"
      uart_event_task_stack_size: 2048
      uart_event_task_priority: 5
      uart_event_queue_size: 30
      tx_buffer_size: 512
      rx_buffer_size: 1024

**Example configuration for a BG96 modem**:

.. code-block:: yaml

    modem:
      type: BG96
      tx_pin: GPIO17
      rx_pin: GPIO16
      reset_pin: GPIO5
      power_pin: GPIO4
      pwrkey_pin: GPIO0
      apn: "internet"
      uart_event_task_stack_size: 2048
      uart_event_task_priority: 5
      uart_event_queue_size: 30
      tx_buffer_size: 512
      rx_buffer_size: 1024

See Also
--------

- :doc:`network`
- :doc:`text_sensor/modem_info`
- :apiref:`modem/modem_component.h`
- `ESP32 Modem connection info <https://pcbartists.com/design/embedded/esp32-modem-connection-schematic-design/>`__
- :ghedit:`Edit`
