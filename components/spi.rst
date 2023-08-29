.. _spi:

SPI Bus
=======

.. seo::
    :description: Instructions for setting up an SPI bus in ESPHome
    :image: spi.svg
    :keywords: SPI

SPI is a very common high-speed protocol for a lot of devices. The ESPHome SPI component implements only the controller
role, where it controls the bus, and writes or reads data from peripherals attached to the bus.

The SPI bus usually consists of 4 wires:

- **CLK**: Is used to tell the receiving device when to read data. All devices on the bus can
  share this line. Sometimes also called ``SCK``.
- **CS** (chip select): Is used to tell the receiving device when it should listen for data. Each device has
  an individual CS line. Sometimes also called ``SS``. If the SPI bus has a single device, its CS pin
  can sometimes be connected to ground to tell it that it is always selected.
- **MOSI** (aka SDO - Serial Data Out): Is used to send data from the controller (the ESP) to the peripheral device.
  All devices on the bus share this line.
- **MISO** (also SDI - Serial Data In): Is used to receive data. All devices on the bus share this line.

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
- **force_sw** (*Optional*, boolean): Whether software implementation should be used even if hardware one is available.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this SPI hub if you need multiple SPI hubs.

**Please note:** while both ESP8266 and ESP32 support the reassignment of the default SPI pins to other GPIO pins, using the dedicated SPI pins can improve performance and stability for certain ESP/device combinations. The ESP8266 supports only one SPI bus,
while the ESP32 supports 2. Additional software SPI buses can be configured, but the maximum achievable data rate with
the software implementation is less than 1MHz.

.. _spi_device:

Other components that depend on the SPI component will reference the SPI component, typically to communicate with specific
peripheral devices. There is also a general-purpose SPI device component that can be used to talk to devices not
supported by a specific component. It allows selection of the SPI bus mode, data_rate, CS pin and bit order.
Reads and writes on the device can be performed with lambdas. For example:

.. code-block:: yaml

    spi:
        clk_pin: GPIO14
        mosi_pin: GPIO27
        miso_pin: GPIO26

    spi_device:
        id: spidev
        data_rate: 2MHz
        mode: 3
        bit_order: lsb_first

   on...:
     then:
       - lambda: !lambda |-
           id(spidev).enable();
           id(spidev).write_byte(0x4F);
           id(spidev).disable();


Configuration variables:
------------------------

- **data_rate** (*Optional*): Set the data rate of the SPI interface. One of ``80MHz``, ``40MHz``, ``20MHz``, ``10MHz``,
  ``5MHz``, ``4MHz``, ``2MHz``, ``1MHz`` (default), ``200kHz``, ``75kHz`` or ``1kHz``. A numeric value in Hz can alternatively
  be specified.
- **mode** (*Optional*): Set the SPI mode - one of ``mode0``, ``mode``, ``mode2``, ``mode3``. The default is ``mode3``.
- **bit_order** (*Optional*): Set the SPI bit order - choose one of ``msb_first`` (default) or ``lsb_first``.
- **cs_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The CS pin.


See Also
--------

- :apiref:`spi/spi.h`
- :ghedit:`Edit`
