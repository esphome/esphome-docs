IR Transmitter Component
========================

The IR transmitter component lets you send infrared messages to control devices in your home.
First, you need to setup a global hub that specifies which pin your IR
led is connected to. Afterwards you can create :doc:`individual
switches </esphomeyaml/components/switch/ir_transmitter>` that
each send a pre-defined IR code to a device.

.. note::

    This component is *much* more accurate on the ESP32, since that chipset has a dedicated
    peripheral for sending exact signal sequences.

.. code:: yaml

    # Example configuration entry
    ir_transmitter:
      - id: 'ir_hub1'
        pin: 32

    # Individual switches
    switch:
      - platform: ir_transmitter
        ir_transmitter_id: 'ir_hub1'
        name: "Panasonic TV Off"
        panasonic:
          address: 0x4004
          command: 0x100BCBD

Configuration variables:
------------------------

-  **pin** (**Required**, :ref:`config-pin`): The pin of the IR LED.
-  **carrier_duty_percent** (*Optional*, int): The duty percentage of
   the carrier. 50 for example means that the LED will be on 50% of the
   time. Must be in range from 1 to 100. Defaults to 50.
-  **id** (*Optional*, :ref:`config-id`): Manually specify
   the ID used for code generation. Use this if you have multiple IR
   transmitters.

See Also
--------

- :doc:`API Reference </api/switch/ir-transmitter>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/ir_transmitter.rst>`__
