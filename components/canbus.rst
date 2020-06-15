.. _canbus:

CAN bus
=======

.. seo::
    :description: Instructions for setting up an CAN bus in ESPHome
    :image: canbus.png
    :keywords: CAN

Controller Area Network (CAN bus) is a serial bus protocol that allows components to communicate on a single or dual-wire networked data bus up to 1Mbps.

The current ESPHome CAN bus implementation supports single frame data transfer. In this way you may send and receive data up to 8 bits.
With this you can transmit the state of a button or the feedback from a sensor on the bus.
All other devices on the bus will be able to get this data to switch on/off a light or display the transmitted data.

You may add multiple busses to you configuration. At this moment only the MCP2515 hardware driver is supported. 

CAN bus Configuration;

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **sender_id** (**Required**, numeric id): With this numeric id we are able to determine the sender.
- **bit_rate** (*Optional*, choose one of the supported CAN bus bitrates): this defaults to 125KBPS.

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

.. warning::

    The cheap MCP2515 devices have a 5V transceiver chip that will not work with 3.3V.

The MCP2515 is a spi device :ref:`SPI Bus <spi>`, so you need to have
a ``spi:`` section in your config for this integration to work.

.. code-block:: yaml

    # example esp8266 spi configuration
    spi:
        clk_pin: D5 #gpio14
        mosi_pin: D7 #gpio13
        miso_pin: D6 #gpio12


MCP2515 Configuration.

- **cs_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): Is used to tell the receiving SPI device when it should listen for data on the SPI bus. Each device has an individual CS line. Sometimes also called ``SS``.
- **clock** (*Optional*, one of the supported values): clock christal used on the MCP2515 device; defaults to 8MHZ. valid values are:

  - 20MHZ
  - 16MHZ
  - 8MHZ
- **mode** (*Optional*, Operation mode for the MCP2515 device):

  - NORMAL: Normal operation
  - LOOPBACK: Loopback mode can be used to just test you spi connection to the device
  - LISTENONLY: only receive data

.. code-block:: yaml

    # example esp8266 spi configuration
    spi:
        clk_pin: D5 #gpio14
        mosi_pin: D7 #gpio13
        miso_pin: D6 #gpio12
    
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

    binary_sensor:
    - platform: gpio
        id: button
        name: button
        pin: 
        number: 0
        inverted: True
        on_press:
        then:
            - canbus.send:
                canbus_id: first_canbus
                can_id: 401
                data: !lambda
                return {100, id(button).state};
        on_release:
        then:
            - canbus.send:
                canbus_id: first_canbus
                can_id: 402
                data: !lambda
                return {255, id(button).state};
        on_click:
        then:
            - canbus.send:
                canbus_id: first_canbus
                can_id: 400
                data: "sender  "

.. _canbus-on_frame:

``on_frame`` Trigger
----------------------

With this configuration option you can write complex automations whenever a CAN bus
message on a specific canid is received. To use the frame content, use a :ref:`lambda <config-lambda>`
template, the frame data is available under the name ``x`` inside that lambda.

.. code-block:: yaml

    canbus:
      - platform: mcp2515
        # ...
        on_frame:
          - can_id: 500
            then:
              - lambda: |-
                  std::string b(x.begin(), x.end());
                  ESP_LOGD("canid 500", "%s", &b[0] );
              - light.turn_off: light_1
        on_frame:
          - can_id: 501
            then:
              - light.turn_on:
                  id: light_1
                  brightness: !lambda "return (float) x[0]/255;"

Configuration variables:

- **can_id** (**Required**, integer): The CAN bus id to listen for. Every time a frame with **this exact id** is received, the automation will trigger.

.. note::

    You can even specify multiple ``on_message`` triggers by using a YAML list:

    .. code-block:: yaml

        mqtt:
          on_message:
             - topic: some/topic
               then:
                 - # ...
             - topic: some/other/topic
               then:
                 - # ...

.. note::

    This action can also be used in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        App.get_mqtt_client()->subscribe("the/topic", [=](const std::string &payload) {
            // do something with payload
        });

See Also
--------

- :apiref:`spi/spi.h`
- :ghedit:`Edit`
