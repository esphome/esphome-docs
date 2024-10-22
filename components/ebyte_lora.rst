Ebyte Lora
=============

.. seo::
    :description: Instructions for setting up a Ebyte Lora component on ESPHome
    :image: ebyte_lora.png
    :keywords: Lora, Ebyte

The purpose of this component is to allow ESPHome nodes to directly communicate with each using LoRa.
It permits the state of sensors and binary sensors to be repeated, and send to individual ESPHome nodes, 
that might be miles away from any active internet connection.

Nodes have a *network_id* to indicate who *they* are, which can mean that they can receive sensor data from one or more
nodes directly or get repeated messages from a repeater node, which can also be a receiver/transmitter.

It has 3 basic primitives:
- Repeater, repeat any message
- Receiver, get some information and do something with it
- Transmitter, send some information

.. code-block:: yaml

    # Example configuration entry
  ebyte_lora:
    id: lora_uart
    uart_id: uart_bus
    recycle_time : 60s
    network_id: 1
    repeater: false 
    pin_aux: GPIO4 
    pin_m0: GPIO1 
    pin_m1: GPIO2
    addl: 04
    channel: 23
    enable_rssi: EBYTE_ENABLED
    lora_rssi:
      name: "Lora RSSI"

Configuration variables:
------------------------

- **id** (**Required**, :ref:`config-id`): The id of the module.
- **uart_id** (**Required**, :ref:`config-id`): Uart bus id used.
- **recycle_time** (*Optional*, :ref:`config-time`): Interval between full broadcasts of all info it contains. Defaults to 10 min. Keep duty cycle in mind!
- **network_id** (**Required**, int): Network id to indicate to the nodes who you are, keep this number unique for each node in your network.
- **repeater** (*Optional*, boolean): Is this module going to repeat any message it receives. Defaults to false.
- **pin_aux** (**Required**,  :ref:`config-pin`): Pin connected to the AUX port on the ebyte module.
- **pin_m0** (**Required**,  :ref:`config-pin`): Pin connected to the M0 port on the ebyte module.
- **pin_m1** (**Required**,  :ref:`config-pin`): Pin connected to the M1 port on the ebyte module.
- **addh** (*Optional*, int): ebyte ADDH. Defaults to 0.
- **addl** (*Optional*, int): ebyte ADDH. Defaults to 0.
- **channel** (*Optional*, int): channel selection. Defaults to 13.
- **uart_bps** (*Optional*, enum):  What speed you set UART to, no need to change. Defaults to ``UART_9600``

  - ``UART_1200`` (1200 bps)
  - ``UART_2400`` (2400 bps)
  - ``UART_4800`` (4800 bps)
  - ``UART_9600`` (4800 bps)
  - ``UART_19200`` (19200 bps)
  - ``UART_38400`` (38400 bps)
  - ``UART_57600`` (57600 bps)
  - ``UART_115200`` (115200 bps)

- **uart_parity** (*Optional*, enum):  Parity to be used. Defaults to ``EBYTE_UART_8N1``

  - ``EBYTE_UART_8N1`` (EBYTE_UART_8N1)
  - ``EBYTE_UART_8O1`` (EBYTE_UART_8O1)
  - ``EBYTE_UART_8E1`` (EBYTE_UART_8E1)

- **transmission_power** (*Optional*, enum):  Power to transmit at. Defaults to ``TX_DEFAULT_MAX``

  - ``TX_DEFAULT_MAX`` (Full power)
  - ``TX_LOWER`` (Lower then full power)
  - ``TX_EVEN_LOWER`` (Even lower then full power db)
  - ``TX_LOWEST`` (Lowest db)

- **air_data_rate** (*Optional*, enum):  The air rate, must be the same for all nodes, higher rate is smaller delay and shorter distance. Defaults to ``AIR_2_4KB``
 
  - ``AIR_2_4KB`` (2.4k)
  - ``AIR_4_8KB`` (4.8k)
  - ``AIR_9_6KB`` (9.6k)
  - ``AIR_19_2KB`` (19.2k)
  - ``AIR_38_4KB`` (38.4k)
  - ``AIR_62_5KB`` (62.4k)

- **sub_packet** (*Optional*, enum):  The data sent is less then this length then it will always output it in one go. Defaults to ``SUB_200B``
  
  - ``SUB_200B`` (200 bytes)
  - ``SUB_128B`` (128 bytes)
  - ``SUB_64B`` (64 bytes)
  - ``SUB_32B`` (32 bytes)

- **wor_period** (*Optional*, enum):  WOR cycle, not implemented. Defaults to ``WOR_4000``

  - ``WOR_500`` (EBYTE_UART_8O1)
  - ``WOR_1000`` (WOR_4000)
  - ``WOR_1500`` (EBYTE_UART_8N1)
  - ``WOR_2000`` (EBYTE_UART_8O1)
  - ``WOR_2500`` (WOR_4000)
  - ``WOR_3000`` (EBYTE_UART_8N1)
  - ``WOR_3500`` (EBYTE_UART_8O1)
  - ``WOR_4000`` (WOR_4000)

- **transmission_mode** (*Optional*, enum):  Fixed or Transparent transmission, fixed is not implemented yet. Defaults to ``TRANSPARENT``
  
  - ``TRANSPARENT`` (Transparent mode)
  - ``FIXED`` (Fixed mode)

- **enable_rssi** (*Optional*, enum): Send a RSSI byte as last byte, keep the same on all nodes. Defaults to ``EBYTE_ENABLED``
  
  - ``EBYTE_ENABLED`` (Enable this setting)
  - ``EBYTE_DISABLED`` (Disable this setting)

- **enable_lbt** (*Optional*, enum): monitoring before sending data, which might help with interference. Defaults to ``EBYTE_DISABLED``
  
  - ``EBYTE_ENABLED`` (Enable this setting)
  - ``EBYTE_DISABLED`` (Disable this setting)

- **rssi_noise** (*Optional*, enum):  Makes it possible to see ambient noise, not yet implemented . Defaults to ``EBYTE_DISABLED``
  
  - ``EBYTE_ENABLED`` (Enable this setting)
  - ``EBYTE_DISABLED`` (Disable this setting)

- **sensors** (*Optional*, list): A list of sensor IDs to be broadcast. Each entry may be just the sensor id, or may set a different id to be broadcast.

  - **id** (**Required**, :ref:`config-id`): The id of the sensor to be used
  - **broadcast_id** (*Optional*, string): The id to be used for this sensor in the broadcast. Defaults to the same as the internal id.

- **binary_sensors** (*Optional*, list): A list of binary sensor IDs to be broadcast.

  - **id** (**Required**, :ref:`config-id`): The id of the binary sensor to be used
  - **broadcast_id** (*Optional*, string): The id to be used for this binary sensor in the broadcast. Defaults to the same as the internal id.


Reliability
-----------

Data will be send every **recycle_time** or whenever a sensor is updated, but this will not guarantee delivery, we do not send any acknowledgement. 
As long as the nodes are within reach of each other or the repeater is setup correctly, it should just work, you can set up UART debug to try and see if information is send.


Configuration examples
----------------------

This example couples two light switches in two different devices, so that switching either one on or off will cause
the other to follow suit. In each case a template binary_sensor is used to mirror the switch state.

.. code-block:: yaml

    # Device 1
  uart:
    id: uart_bus
    tx_pin: GPIO43 #D6
    rx_pin: GPIO44 #D7
    baud_rate: 9600
    debug:
      direction: BOTH
      dummy_receiver: false
      after:
        delimiter: "\n"
      sequence:
        - lambda: UARTDebug::log_hex(direction, bytes, ':');
    esphome:
      name: device-1
    ebyte_lora:
      id: lora_uart
      uart_id: uart_bus
      network_id: 1
      repeater: false 
      pin_aux: GPIO4 
      pin_m0: GPIO1 
      pin_m1: GPIO2
      addl: 04
      channel: 23
      binary_sensors:
        - relay1_sensor

    switch:
      - platform: gpio
        pin: GPIO6
        id: relay1
        name: "Device 1 switch"

    binary_sensor:
      - platform: template
        id: relay1_sensor
        lambda: "return id(relay1).state;"

      - platform: ebyte_lora
        network_id: 2
        id: relay2_sensor
        on_press:
          switch.turn_on: relay1
        on_release:
          switch.turn_off: relay1


    # Device 2
  uart:
    id: uart_bus
    tx_pin: GPIO43 #D6
    rx_pin: GPIO44 #D7
    baud_rate: 9600
    debug:
      direction: BOTH
      dummy_receiver: false
      after:
        delimiter: "\n"
      sequence:
        - lambda: UARTDebug::log_hex(direction, bytes, ':');
    esphome:
      name: device-2

    ebyte_lora:
      id: lora_uart
      uart_id: uart_bus
      network_id: 2
      repeater: false 
      pin_aux: GPIO4 
      pin_m0: GPIO1 
      pin_m1: GPIO2
      addl: 04
      channel: 23
      binary_sensors:
        - relay2_sensor

    switch:
      - platform: gpio
        pin: GPIO6
        id: relay2
        name: "Device 2 switch"

    binary_sensor:
      - platform: template
        id: relay2_sensor
        lambda: "return id(relay2).state;"

      - platform: ebyte_lora
        network_id: 1
        id: relay1_sensor
        on_press:
          switch.turn_on: relay2
        on_release:
          switch.turn_off: relay2


See Also
--------

- :ref:`automation`
- :apiref:`ebyte_lora/ebyte_lora_component.h`
- :ghedit:`Edit`
