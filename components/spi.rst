.. _spi:

SPI Bus
=======

.. seo::
    :description: Instructions for setting up an SPI bus in ESPHome
    :image: spi.svg
    :keywords: SPI

SPI is a very common high-speed protocol for a lot of devices. The SPI bus usually consists of 4 wires:

- **CLK**: Is used to tell the receiving device when to read data. All devices on the bus can
  share this line. Sometimes also called ``SCK``.
- **CS** (chip select): Is used to tell the receiving device when it should listen for data. Each device has
  an individual CS line. Sometimes also called ``SS``. If the SPI bus has a single device, its CS pin
  can sometimes be connected to ground to tell it that it is always selected.
- **MOSI** (also DIN): Is used to send data from the master (the ESP) to the receiving device. All devices on the bus can
  share this line.
- **MISO** (also DOUT): Is used to receive data. All devices on the bus can
  share this line.

In some cases one of **MOSI** or **MISO** do not exist as the receiving device only accepts data or sends data.

To set up SPI devices in ESPHome, you first need to place a top-level SPI hub like below which defines what pins to
use for the functions described above. The **CS** pins are then individually managed by the components. The ``spi:``
component also accepts a list of buses if you want to have multiple SPI buses with your ESP (though this should
rarely be necessary, as the SPI bus can be shared by the devices).

.. code-block:: yaml

    # Example configuration entry
    spi:
      clk_pin: GPIO14
      mosi_pin: GPIO13
      miso_pin: GPIO12

Configuration variables:
------------------------

- **clk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin used for the clock line of the SPI bus.
- **mosi_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin used for the MOSI line of the SPI bus.
- **miso_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin used for the MISO line of the SPI bus.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this SPI hub if you need multiple SPI hubs.

See Also
--------

- :apiref:`spi/spi.h`
- :ghedit:`Edit`
