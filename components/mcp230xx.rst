MCP230xx I/O Expander
=====================

.. seo::
    :description: Instructions for setting up MCP23008, MCP23016 or MCP23017 digital port expander in ESPHome.
    :image: mcp230xx.png

The Microchip MCP230xx series of general purpose, parallel I/O expansion for I²C bus applications.

**Supported Variants :**

- :ref:`mcp23008-label`
- :ref:`mcp23016-label`
- :ref:`mcp23017-label`

.. _mcp23008-label:

MCP23008 Component
------------------

The MCP23008 component (`datasheet <http://ww1.microchip.com/downloads/en/devicedoc/21919e.pdf>`__,
`Adafruit <https://www.adafruit.com/product/593>`__) has 8 GPIOs that can be configured independently.

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
          mcp23xxx: mcp23008_hub
          # Use pin number 0
          number: 0
          mode: OUTPUT
          inverted: False

    # Individual inputs
    binary_sensor:
      - platform: gpio
        name: "MCP23008 Pin #1"
        pin:
          mcp23xxx: mcp23008_hub
          # Use pin number 1
          number: 1
          # One of INPUT or INPUT_PULLUP
          mode: INPUT
          inverted: False

Configuration variables:
************************

- **id** (**Required**, :ref:`config-id`): The id to use for this MCP23008 component.
- **address** (*Optional*, int): The I²C address of the driver.
  Defaults to ``0x20``.
- **open_drain_interrupt** (*Optional*, bool): Configure the interrupt pin to open-drain mode.
  Useful when the MCP23008's power supply is greater than 3.3 volts. Note that this pin
  will require a pull-up resistor (to 3.3 volts) when this mode is enabled.

Pin configuration variables:
****************************

- **mcp23xxx** (**Required**, :ref:`config-id`): The id of the MCP23008 component.
- **interrupt** (*Optional*): Set this pin to trigger the INT pin on the component. Can be one of ``CHANGE``, ``RISING``, ``FALLING``.
- **number** (**Required**, integer): The pin number.
- **inverted** (*Optional*, boolean): If all read and written values
  should be treated as inverted. Defaults to ``False``.
- **mode** (*Optional*, string): A pin mode to set for the pin at. One of ``INPUT`` or ``OUTPUT``.

.. _mcp23016-label:

MCP23016 Component
------------------

The MCP23016 component (`datasheet <http://ww1.microchip.com/downloads/en/devicedoc/20090c.pdf>`__)
has 16 GPIOs and can be configured the same way than the other variants.

.. note::

    The 'INPUT_PULLUP' mode is not supported on this device.

.. code-block:: yaml

    # Example configuration entry
    mcp23016:
      - id: 'mcp23016_hub'
        address: 0x20

    # Individual outputs
    switch:
      - platform: gpio
        name: "MCP23016 Pin #0"
        pin:
          mcp23016: mcp23016_hub
          # Use pin number 0
          number: 0
          mode: OUTPUT
          inverted: False

    # Individual inputs
    binary_sensor:
      - platform: gpio
        name: "MCP23016 Pin #1"
        pin:
          mcp23016: mcp23016_hub
          # Use pin number 1
          number: 1
          mode: INPUT
          inverted: False


Configuration variables:
************************

- **id** (**Required**, :ref:`config-id`): The id to use for this MCP23016 component.
- **address** (*Optional*, int): The I²C address of the driver.
  Defaults to ``0x20``.

Pin configuration variables:
****************************

- **mcp23xxx** (**Required**, :ref:`config-id`): The id of the MCP23016 component.
- All other options from :ref:`Pin Schema <config-pin_schema>`


.. _mcp23017-label:

MCP23017 Component
------------------

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
          mcp23xxx: mcp23017_hub
          # Use pin number 0
          number: 0
          mode: OUTPUT
          inverted: False

    # Individual inputs
    binary_sensor:
      - platform: gpio
        name: "MCP23017 Pin #1"
        pin:
          mcp23xxx: mcp23017_hub
          # Use pin number 1
          number: 1
          # One of INPUT or INPUT_PULLUP
          mode: INPUT_PULLUP
          inverted: False

Configuration variables:
************************

- **id** (**Required**, :ref:`config-id`): The id to use for this MCP23017 component.
- **address** (*Optional*, int): The I²C address of the driver.
  Defaults to ``0x20``.
- **open_drain_interrupt** (*Optional*, bool): Configure interrupt pins to open-drain mode.
  Useful when the MCP23017's power supply is greater than 3.3 volts. Note that these pins
  will require pull-up resistors (to 3.3 volts) when this mode is enabled.

Pin configuration variables:
****************************

- **mcp23xxx** (**Required**, :ref:`config-id`): The id of the MCP23017 component.
- **interrupt** (*Optional*): Set this pin to trigger the port INT pin on the component. Can be one of ``CHANGE``, ``RISING``, ``FALLING``.
- All other options from :ref:`Pin Schema <config-pin_schema>`


See Also
--------

- :ref:`i2c`
- :doc:`switch/gpio`
- :doc:`binary_sensor/gpio`
- :apiref:`API Reference (MCP23008) <mcp23008/mcp23008.h>`
- :apiref:`API Reference (MCP23016) <mcp23016/mcp23016.h>`
- :apiref:`API Reference (MCP23017) <mcp23017/mcp23017.h>`
- :ghedit:`Edit`
