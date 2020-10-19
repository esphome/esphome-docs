Midea Air Conditioner
=====================

.. seo::
    :description: Instructions for setting up a Midea climate device
    :image: air-conditioner.png

The ``midea_ac`` component creates a air conditioner climate device.

This component requires a :doc:`/components/midea_dongle` to be configured.

Example of hardware implementation is `Midea Open Dongle <https://github.com/dudanov/midea-open-dongle>`_ in free `KiCad <https://kicad-pcb.org>`_ format.

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

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **midea_dongle_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`/components/midea_dongle` if you want to use multiple devices.
- **name** (**Required**, string): The name of the climate device.
- **beeper** (*Optional*, bool, default: **false**): Beeper feedback on command.
- All other options from :ref:`Climate <config-climate>`.

See Also
--------

- :doc:`/components/midea_dongle`
- :doc:`/components/climate/index`
- :apiref:`climate/midea_ac.h`
- :ghedit:`Edit`
