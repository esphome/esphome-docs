Midea Dongle
============

.. seo::
    :description: Instructions for setting up the Midea Dongle component
    :image: midea.svg
    :keywords: midea

The ``midea_dongle`` component creates a serial connection to the Midea climate devices for platforms to use.

As the communication with Midea devices done using UART, you need
to have an :ref:`UART bus <uart>` in your configuration.
Additionally, you need to set the baud rate to 9600.

.. code-block:: yaml

    # Example configuration entry
    # Disable logging over UART
    logger:
      baud_rate: 0

    uart:
      tx_pin: 1
      rx_pin: 3
      baud_rate: 9600

    midea_dongle:

    midea_ac:
      name: "Midea AC"
      beeper: true

.. note::

    The configuration above should work for Midea air conditioner.

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

See Also
--------

- :ref:`sensor-filters`
- :apiref:`cse7766/cse7766.h`
- :ghedit:`Edit`
