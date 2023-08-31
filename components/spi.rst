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
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this SPI hub if you need multiple SPI hubs.
- **interface** (*Optional*): Controls which hardware or software SPI interface should be used.
  Value may be one of ``any`` (default), ``software`` or a number corresponding to a hardware interface.
  See discussion below.
- **force_sw** (*Optional*, **Deprecated**, boolean): Whether software implementation should be used even if a hardware
  interface is available. Default is ``false``.

Interface selection:
--------------------

ESP32 and ESP8266 chips have several hardware SPI controller interfaces - usually the first one or two are reserved for use to access
the flash and PSRAM memories, leaving one or two user-accessible SPI controllers. An SPI hub configured in
ESPHome can be assigned to one of these interfaces with the ``interface:`` configuration option.

The numbering of
these interfaces in the YAML configuration starts with 0, corresponding to the first user-accessible SPI controller. Check the datasheet
for a given chip to determine which this is, but it will typically be ``SPI1`` on ESP8266 and ``SPI2`` on ESP32. Any further
available interfaces will be sequentially numbered. Unless you have a particular need to choose a specific interface
just leave this option at the default of ``any``.

If the ``software`` option is chosen, or you configure more SPI hubs than there are available hardware controllers,
the remaining hubs will use a software implementation, which is unable to achieve data rates above a few hundred
kHz.

While the ESP32 supports the reassignment of the default SPI pins to most other GPIO pins, using the dedicated SPI pins can improve performance and stability for certain ESP/device combinations. ESP8266 has a more limited selection of pins that can be used, again
check the datasheet for more information.

Generic SPI device component:
-----------------------------
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
        cs_pin: GPIO13
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
- **mode** (*Optional*): Set the SPI mode - one of ``mode0``, ``mode1``, ``mode2``, ``mode3``. The default is ``mode3``.
  See table below for more information
- **bit_order** (*Optional*): Set the SPI bit order - choose one of ``msb_first`` (default) or ``lsb_first``.
- **cs_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The CS pin.

SPI modes:
----------

SPI devices operate in one of four modes as per the table below. Mode 3 is the most commonly used.

.. csv-table:: Supported Modes
    :header: "Mode", "Clock Idle Polarity", "Clock Phase", "Data shifted on", "Data sampled on"

    "0", "low", "leading", "/CS activation and falling CLK", "rising CLK"
    "1", "low", "trailing", "rising CLK", "falling CLK"
    "2", "high", "leading", "/CS activation and rising CLK", "falling CLK"
    "3", "high", "trailing", "falling CLK", "rising CLK"



See Also
--------

- :apiref:`spi/spi.h`
- :ghedit:`Edit`
