Relay
=====

.. seo::
    :description: Instructions for using the M5Stack 4Relay with ESPHome.
    :image: m5stack_4relay.webp
    :keywords: Relay, M5Stack 4Relay

.. figure:: images/m5stack_4relay.webp
    :align: center
    :width: 80.0%

The M5Stack 4Relay is a module consisting of four electromechanical relays and an
STM32 MCU. The MCU controls the state of each relay and speaks a simple I2C protocol.

Detailed documentation on the device is available at `<https://docs.m5stack.com/en/unit/4relay?id=description>`

.. code-block:: yaml

    m5stack_4relay:
        address: 0x26
    
    
    switch:
        - platform: m5stack_4relay
          id: relay_1
          channel: 0
          name: Relay 1
        - platform: m5stack_4relay
          id: relay_2
          channel: 1
          name: Relay 2
        - platform: m5stack_4relay
          id: relay_3
          channel: 2
          name: Relay 3
        - platform: m5stack_4relay
          id: relay_4
          channel: 3
          name: Relay 4


See Also
--------

- :doc:`/components/switch/gpio`
- :doc:`/components/output/gpio`
- :doc:`/cookbook/relay`
- `How do relays work <https://www.explainthatstuff.com/howrelayswork.html>`__.
- :ghedit:`Edit`
