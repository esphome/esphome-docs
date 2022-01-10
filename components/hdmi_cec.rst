HDMI-CEC Component
==================

.. seo::
    :description: Instructions for setting up HDMI-CEC in ESPHome.
    :image: hdmi-cec.png

The ``hdmi_cec`` component enables receiving and transmitting HDMI-CEC messages to connected HDMI
devices.

This can be used to read HDMI-CEC commands from other devices (e.g. volume, power on, input
changed) as well as send your own commands onto the HDMI-CEC bus.

For example, you can use this integration to pretend to be an audio device, intercept HDMI-CEC
volume commands and transmit the IR codes to control older sound equipment.


Configuration variables
-----------------------

- **pin** (**Required**, :ref:`config-pin`): The pin on your device you will connect to the HDMI
  CEC pin.
- **address** (**Required**, integer 0-14): The initial logical address of the device. This corresponds to the device class
  you are impersonating (e.g. 0x0 for TV, 0x5 for audio). This may be
  reassigned if there are other devices of the same type on the CEC bus. See here https://kwikwai.com/knowledge-base/the-hdmi-cec-bus/
- **physical_address** (*Optional*, integer 0-65534): The physical address represents where this device is connected in the
  point-to-point topology of the HDMI connections. This is discovered using the HDMI DDC connection.
  We don't have access to this exchange so this must be hardcoded. It can be worth experimenting
  with this value if your HDMI devices aren't recognizing your ESPHome.
- **promiscuous_mode** (*Optional*, boolean): By default messages that
  aren't addressed to our logical address are dropped. By enabling ``promiscuous_mode`` you can
  intercept messages between other devices (e.g. between your TV and Bluray player).
- **on_message** (*Optional*, :ref:`Automation <automation>`): One or more automations to call when
  Messages are received. These can be filtered based on source address, destination address,
  opcode, or message data. See :ref:`config-on_message`.

.. _config-on_message:

On Message
----------

Incoming messages can be filtered and specific automations can execute if all filter criteria
are met.

- **source** (*Optional*, integer 0-15): Logical address of the device that sent the message.
- **destination** (*Optional*, integer 0-15): Logical address of the device that the message is
  being sent to.
- **opcode** (*Optional*, integer 0-255): Opcode byte of the message.
- **data** (*Optional*, list of bytes): List of bytes in the message (without the
  source/destination header byte).


Wiring
------

HDMI-CEC is a 3.3V protocol, so no external components are needed since the ESP* chips have 3.3V IO.
A [HDMI breakout connector](https://www.amazon.com/gp/product/B075Q8HG2B) might be handy though.
Since HDMI-CEC is a bus, all devices should be electrically connected on HDMI pin 13, so anywhere
you can tap into that pin should work. You could plug into any available HDMI port, or splice into
a cable between two devices. Just connect:

* GPIO of your choice to HDMI pin 13
* GND from the ESP board to HDMI pin 17 (DDC/CEC Ground)

Additionally, if you're plugging directly into an HDMI port (and not splicing a cable between
an existing source and sink) you will probably also want to connect pin 18 to 5V. This is typtically
how the HDMI sink device (TV or receiver) knows something is connected on that port.


Examples
--------

The following example pretends to be an audio device, receives volume commands over CEC, then
transmits IR codes to a soundbar to control the volume.

.. code-block:: yaml

    esphome:
        name: media-controller
        platform: ESP8266
        board: d1_mini
        platformio_options:
            board_build.f_cpu: 160000000L

    remote_transmitter:
    pin: D0
    carrier_duty_percent: 50%

    hdmi_cec:
        address: 0x05 # Audio system
        physical_address: 0x4000
        pin: D1
        on_message:
            - opcode: 0xC3 # Request ARC start
            then:
                - hdmi_cec.send: # Report ARC started
                    destination: 0x0
                    data: [ 0xC1 ]
            - opcode: 0x70 # System audio mode request
            then:
                - hdmi_cec.send:
                    destination: 0x0
                    data: [ 0x72, 0x01 ]
            - opcode: 0x7D # Give audio system mode status
            then:
                - hdmi_cec.send:
                    destination: 0x0
                    data: [ 0x7E, 0x01 ]
            - opcode: 0x46 # Give OSD name
            then:
                - hdmi_cec.send:
                    destination: 0x0
                    data: [0x47, 0x65, 0x73, 0x70, 0x68, 0x6F, 0x6D, 0x65] # esphome
            - opcode: 0x8C # Give device Vendor ID
            then:
                - hdmi_cec.send:
                    destination: 0xF
                    data: [0x87, 0x00, 0x15, 0x82]
            - data: [0x44, 0x41] # User control pressed: volume up
            then:
                - logger.log: "Volume up"
                - remote_transmitter.transmit_nec:
                    address: 0xFF00
                    command: 0xBE41
            - data: [0x44, 0x42] # User control pressed: volume down
            then:
                - logger.log: "Volume down"
                - remote_transmitter.transmit_nec:
                    address: 0xFF00
                    command: 0xBA45
            - data: [0x44, 0x43] # User control pressed: volume mute
            then:
                - logger.log: "Volume mute"
                - remote_transmitter.transmit_nec:
                    address: 0xFF00
                    command: 0xB748

Notes
-----

The timing for receiving and parsing CEC messages depends on the timing with which ``loop`` is called
and thus this is sensitive to other things the microcontroller is doing that may delay the ``loop``
method getting called. On the ESP8266 it's a good idea to bump the CPU speed to 160MHz:

.. code-block:: yaml

    esphome:
    ...
    platformio_options:
        board_build.f_cpu: 160000000L

In the future this could be improved by better use of interrupts in the underlying CEC library.


See Also
--------

- :apiclass:`:hdmi_cec::HdmiCec`
- `CEC-O-MATIC reference for CEC messages <https://www.cec-o-matic.com>`__
- `HDMI 1.3a Spec <https://web.archive.org/web/20171009194844/http://www.microprocessor.org/HDMISpecification13a.pdf>__`
- :ghedit:`Edit`
