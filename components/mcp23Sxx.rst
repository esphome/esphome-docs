MCP23Sxx I/O Expander
=====================

.. seo::
    :description: Instructions for setting up MCP23S08, MCP23S16 or MCP23S17 digital port expander in ESPHome. This is exactly the same API as the MCP23SXX I/O Expander except talks on the SPI bus
    :image: mcp23Sxx.png

The Microchip MCP23Sxx series of general purpose, parallel I/O expansion for SPI bus applications.
This is exactly the same API as the MCP23SXX I/O Expander except talks on the SPI bus

**Supported Variants :**

- :ref:`mcp23S08-label`
- :ref:`mcp23S17-label`

.. _mcp23S08-label:

MCP23S08 Component
------------------

The MCP23S08 component (`datasheet <http://ww1.microchip.com/downloads/en/DeviceDoc/MCP23008-MCP23S08-Data-Sheet-20001919F.pdf>`__,
`Digi-Key <https://www.digikey.com/product-detail/en/microchip-technology/MCP23S08-E-P/MCP23S08-E-P-ND/735954>`__) has 8 GPIOs that can be configured independently.

.. code-block:: yaml

    # Example configuration entry
    mcp23s08:
      - id: 'mcp23s08_hub'
        cs_pin: D8
        deviceaddress: 0

    # Individual outputs
    switch:
      - platform: gpio
        name: "MCP23S08 Pin #0"
        pin:
          mcp23xxx: mcp23s08_hub
          # Use pin number 0
          number: 0
          # One of INPUT, INPUT_PULLUP or OUTPUT
          mode: OUTPUT
          inverted: False

    # Individual inputs
    binary_sensor:
      - platform: gpio
        name: "MCP23S08 Pin #1"
        pin:
          mcp23xxx: mcp23s08_hub
          # Use pin number 1
          number: 1
          # One of INPUT or INPUT_PULLUP
          mode: INPUT
          inverted: False

Configuration variables:
************************

- **id** (**Required**, :ref:`config-id`): The id to use for this MCP23S08 component.
- **cs_pin** (**Required**, int): The SPI chip select pin to use
- **deviceaddress** (*Optional*, int): The address of the chip.
  Defaults to ``0``.
- **open_drain_interrupt** (*Optional*, bool): Configure interrupt pins to open-drain mode.
  Useful when the MCP23S08's power supply is greater than 3.3 volts. Note that these pins
  will require pull-up resistors (to 3.3 volts) when this mode is enabled.

Pin Configuration Variables:
****************************

- **mcp23xxx** (**Required**, :ref:`config-id`): The id of the MCP23S08 component.
- **interrupt** (*Optional*): Set this pin to trigger the INT pin on the component. Can be one of ``CHANGE``, ``RISING``, ``FALLING``.
- All other options from :ref:`Pin Schema <config-pin_schema>`


.. _mcp23S17-label:

MCP23S17 Component
------------------

The MCP23S17 component allows you to use MCP23S17 I/O expanders
(`datasheet <http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf>`__,
`Digi-Key <https://www.digikey.com/product-detail/en/microchip-technology/MCP23S17-E-SP/MCP23S17-E-SP-ND/894276>`__) in ESPHome.
It uses the :ref:`SPI Bus <spi>` for communication.

Once configured, you can use any of the 16 pins as
pins for your projects. Within ESPHome they emulate a real internal GPIO pin
and can therefore be used with many of ESPHome's components such as the GPIO
binary sensor or GPIO switch.

.. code-block:: yaml

    # Example configuration entry
    mcp23s17:
      - id: 'mcp23s17_hub'
        cs_pin: D8
        deviceaddress: 0

    # Individual outputs
    switch:
      - platform: gpio
        name: "MCP23S17 Pin #0"
        pin:
          mcp23xxx: mcp23s17_hub
          # Use pin number 0
          number: 0
          mode: OUTPUT
          inverted: False

    # Individual inputs
    binary_sensor:
      - platform: gpio
        name: "MCP23S17 Pin #1"
        pin:
          mcp23xxx: mcp23s17_hub
          # Use pin number 1
          number: 1
          # One of INPUT or INPUT_PULLUP
          mode: INPUT_PULLUP
          inverted: False

Configuration variables:
************************

- **id** (**Required**, :ref:`config-id`): The id to use for this MCP23S17 component.
- **cs_pin** (**Required**, int): The SPI chip select pin to use.
- **deviceaddress** (*Optional*, int): The address of the chip.
  Defaults to ``0``.
- **open_drain_interrupt** (*Optional*, bool): Configure interrupt pins to open-drain mode.
  Useful when the MCP23S17's power supply is greater than 3.3 volts. Note that these pins
  will require pull-up resistors (to 3.3 volts) when this mode is enabled.

Pin Configuration Variables:
****************************

- **mcp23xxx** (**Required**, :ref:`config-id`): The id of the MCP23S17 component.
- **interrupt** (*Optional*): Set this pin to trigger the port INT pin on the component. Can be one of ``CHANGE``, ``RISING``, ``FALLING``.
- All other options from :ref:`Pin Schema <config-pin_schema>`


See Also
--------

- :ref:`spi`
- :doc:`switch/gpio`
- :doc:`binary_sensor/gpio`
- :apiref:`API Reference (MCP23S08) <mcp23S08/mcp23S08.h>`
- :apiref:`API Reference (MCP23S17) <mcp23S17/mcp23S17.h>`
- :ghedit:`Edit`
