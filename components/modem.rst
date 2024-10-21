Modem Component
===============

.. seo::
    :description: Instructions for setting up the Modem configuration for your ESP32 node in ESPHome.
    :image: modem.svg
    :keywords: Modem, ESP32

This ESPHome component enables *cellular* modem connections for ESP32.

This component **not** be used in simultaneously with the Wi-Fi component, or in simultaneously with the Internet component, even if both are physically accessible.

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

  - ``SIM800``

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

**Example configuration for a LilyGo-T-Call-SIM800**:

.. code-block:: yaml

    modem:
      type: SIM800
      tx_pin: 27
      rx_pin: 26
      # reset_pin: 5
      power_pin: 23
      pwrkey_pin: 4

.. note::

    Оn some boards the reset pin does not work. For more details, refer to the [issue discussion](https://github.com/xinyuan-lilygo/lilygo-t-call-sim800/issues/238?ref=https://coder.social).

See Also
--------

- :doc:`network`
- :apiref:`modem/modem_component.h`
- :ghedit:`Edit`
