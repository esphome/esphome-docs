.. _canbus:

CAN bus
=======

.. seo::
    :description: Instructions for setting up an CAN bus in ESPHome
    :image: canbus.png
    :keywords: CAN

Controller Area Network (CAN bus) is a serial bus protocol to connect individual systems and sensors as an alternative to conventional multi-wire looms.
It allows automotive components to communicate on a single or dual-wire networked data bus up to 1Mbps.
CAN is an International Standardization Organization (ISO) defined serial communications bus originally
developed for the automotive industry to replace the complex wiring harness with a two-wire bus. The
specification calls for high immunity to electrical interference and the ability to self-diagnose and repair
data errors. These features have led to CAN’s popularity in a variety of industries including building
automation, medical, and manufacturing.

The current ESPHome implementation supports single frame data transfer. In this way you may send and receive data up to 8 bits.
With this you can transmit the press of a button or the feedback from a sensor on the bus.
All other devices on the bus will be able to get this data to switch on/off a light or display the transmitted data.

The CAN bus itself has only two wires. For the ESPHome CAN bus to work you need to select the device that has the physical CAN bus implemented.
At this moment only the MCP2515 driver is supported. You can configure multiple busses.

The CAN bus is then configured as follows;
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **sender_id** (**Required**, numeric id): numeric id to be able to determine the sender.
- **bit_rate** (*Optional*, one of the supported bitrates): defaults to 125KBPS.

- 5KBPS
- 10KBPS
- 20KBPS
- 31K25BPS
- 33KBPS
- 40KBPS
- 50KBPS
- 80KBPS
- 83K3BPS
- 95KBPS
- 100KBPS
- 125KBPS
- 200KBPS
- 250KBPS
- 500KBPS
- 1000KBPS

MCP2515
-------

The MCP2515 is a spi device and therfore you must first add the configuration for the spi bus to your file.

- **cs_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): Is used to tell the receiving SPI device when it should listen for data on the SPI bus. Each device has an individual CS line. Sometimes also called ``SS``.
- **clock** (*Optional*, one of the supported values): clock christal used on the MCP2515 device; defaults to 8MHZ. valid values:
  - 20MHZ
  - 16MHZ
  - 8MHZ
- **mode** (*Optional*, Operation mode for the MCP2515 device):
  - NORMAL: Normal operation
  - LOOPBACK: Loopback mode can be used to just test you spi connectiens to the device
  - LISTENONLY: only receive data

.. code-block:: yaml

    # Example configuration entry
    canbus:
    - platform: mcp2515
        id: first_canbus
        sender_id: 10
        cs_pin: 15
        bit_rate: 125KBPS
        clock: 8MHZ
        mode: NORMAL
        on_frame:
        - can_id: 500
            then:
            - lambda: |-
                std::string b(x.begin(), x.end());
                ESP_LOGD("canid 500", "%s", &b[0] );
            - light.turn_off: light_1
        - can_id: 501
            then:
            - light.turn_on:
                id: light_1
                brightness: !lambda "return (float) x[0]/255;"
        - can_id: 502
            then:
            - light.turn_on:
                id: light_1
                brightness: !lambda "return (float) x[0]/255;"

See Also
--------

- :apiref:`spi/spi.h`
- :ghedit:`Edit`
