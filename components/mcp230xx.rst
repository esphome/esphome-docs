MCP230xx I/O Expander
=====================

.. seo::
    :description: Instructions for setting up MCP23017 or MCP23008 digital port expanders in ESPHome.
    :image: mcp230xx.png

The Microchip MCP230xx series of general purpose, parallel I/O expansion for I²C
bus applications come in two different variants: the 8-bit MCP23008 and the 16-bit
MCP23017, which provide 8 and 16 additional GPIO pins, respectively.

MCP23017
--------

The MCP23017 component allows you to use MCP23017 I/O expanders
(`datasheet <http://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf>`__,
`Adafruit <https://www.adafruit.com/product/732>`__) in ESPHome.
It uses the :ref:`I²C Bus <i2c>` for communication.

Once configured, you can use any of the 16 pins as
pins for your projects. Within ESPHome they emulate a real internal GPIO pin
and can therefore be used with many of ESPHome's components such as the GPIO
binary sensor or GPIO switch.

.. code-block:: yaml

    # Example configuration entry
    mcp23017:
      - id: 'mcp23017_hub'
        address: 0x20

    # Individual outputs
    switch:
      - platform: gpio
        name: "MCP23017 Pin #0"
        pin:
          mcp23017: mcp23017_hub
          # Use pin number 0
          number: 0
          # One of INPUT, INPUT_PULLUP or OUTPUT
          mode: OUTPUT
          inverted: False

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **id** (**Required**, :ref:`config-id`): The id to use for this MCP23017 component.
- **address** (*Optional*, int): The I²C address of the driver.
  Defaults to ``0x21``.



MCP23008
--------

The configuration is essentially the same with the MCP23017 component
(`datasheet <http://ww1.microchip.com/downloads/en/devicedoc/21919e.pdf>`__,
`Adafruit <https://www.adafruit.com/product/593>`__):

.. code-block:: yaml

    # Example configuration entry
    mcp23008:
      - id: 'mcp23008_hub'
        address: 0x20

    # Individual outputs
    switch:
      - platform: gpio
        name: "MCP23008 Pin #0"
        pin:
          mcp23008: mcp23008_hub
          # Use pin number 0
          number: 0
          # One of INPUT, INPUT_PULLUP or OUTPUT
          mode: INPUT_PULLUP
          inverted: False


Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **id** (**Required**, :ref:`config-id`): The id to use for this MCP23008 component.
- **address** (*Optional*, int): The I²C address of the driver.
  Defaults to ``0x21``.


See Also
--------

- :ref:`i2c`
- :doc:`switch/gpio`
- :doc:`binary_sensor/gpio`
- :apiref:`mcp23017/mcp23017.h`
- :ghedit:`Edit`

