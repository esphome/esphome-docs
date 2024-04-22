Adafruit NeoKey 1x4 QT I2C Breakout
======================================

.. seo::
    :description: Instructions for setting up NeoKey 1x4 breakout board using ESPHome.

The NeoKey 1x4 is a breakout board, running the seesaw firmware, that runs over an I²C bus and has the ability to read key presses and control LEDs.

.. figure:: /images/adafruit_neokey_1x4.jpg
    :align: center
    :width: 50.0%

.. code-block:: yaml

    # Example config
    neokey:

    binary_sensor:
      - platform: neokey
        name: "Key 1"
        key: 0
      - platform: neokey
        name: "Key 2"
        key: 1
      - platform: neokey
        name: "Key 3"
        key: 2
      - platform: neokey
        name: "Key 4"
        key: 3

Configuration variables:
************************

- **id** (*Optional*, :ref:`config-id`): The id to use for the NeoKey component. Required for multiple.
- **address** (*Optional*, int): The I²C address of the board.
  Defaults to ``0x30``.

See Also
--------

- :ref:`i2c`
- :doc:`binary_sensor/neokey`
- :doc:`light/neokey`
- :ghedit:`Edit`
