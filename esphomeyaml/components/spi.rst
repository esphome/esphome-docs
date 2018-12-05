.. _spi:

SPI Bus
=======

.. seo::
    :description: Instructions for setting up an SPI bus in esphomelib
    :image: spi.png
    :keywords: SPI

SPI is a very common high-speed protocol for a lot of devices. The SPI bus usually consists of 4 wires:

- **CLK**: Is used to tell the receiving device when to read data. All devices on the bus can
  share this line. Sometimes also called ``SCK``.
- **CS** (chip select): Is used to tell the receiving device when it should listen for data. Each device has
  an individual CS line. Sometimes also called ``SS``.
- **MOSI** (also DIN): Is used to send data from the master (the ESP) to the receiving device. All devices on the bus can
  share this line.
- **MISO** (also DOUT): Is used to receive data. All devices on the bus can
  share this line.

In some cases one of **MOSI** or **MISO** do not exist as the receiving device only accepts data or sends data.

To set up SPI devices in esphomelib, you first need to place a top-level SPI hub like below which defines what pins to
use for the functions described above. The **CS** pins are then individually managed by the components. The ``spi:``
component also accepts a list of buses if you want to have multiple SPI buses with your ESP (though this should
rarely be necessary, as the SPI bus can be shared by the devices).

.. code-block:: yaml

    # Example configuration entry
    spi:
      clk_pin: GPIO21
      mosi_pin: GPIO22
      miso_pin: GPIO23

Configuration variables:
------------------------

- **clk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin used for the clock line of the SPI bus.
- **mosi_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin used for the mosi line of the SPI bus.
- **miso_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin used for the miso line of the SPI bus.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this SPI hub if you need multiple SPI hubs.

See Also
--------

- :doc:`API Reference </api/core/spi>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/spi.rst>`__

.. disqus::
