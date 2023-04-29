MicroNova based pellet stove
============================

.. seo::
    :description: Instructions for setting up a MicroNova board based pellet stove in ESPHome.

The MicroNova component allows you to integrate a pellet stove with a MicroNova board in ESPHome.
It uses :ref:`UART <uart>` for communication.

The :ref:`UART <uart>` must be configured with a baud rate 1200, 8 data bits, 2 stop bits, no parity, no flow control. 

.. warning::

    The MicroNova bords come in various flavours. This code is only tested on an ExtraFlame Ketty Evo 2.0 stove. The protocol is not
    documented but has been reverse engineerd by others. See the links below for all the info that helped me.
    The different sensors, buttons and stove switch may require specific **memory_location** and **memory_address** parameters that 
    match your MicroNova specific board.

    Also, switching your stove on or off can behave different on the various MicroNova flavours.

    Use this integration at your own risk.

Connecting your stove
---------------------

Most MicroNova based pellet stoves have a serial output. In most cases this output has 4 pins: GND, 5v, 20V and DATA.

.. figure:: images/micronova_serial.png
    :align: center
    :width: 50.0%

.. figure:: images/micronova_serial_layout.png
    :align: center
    :width: 50.0%

You will have to build a simple circuit to interface with your stove. It is based on optocouplers for galvanic separation and logic 
level shifting between 5v and 3V3.

.. figure:: images/micronova_optocouplers.png
    :align: center
    :width: 100.0%

    Optocoupler interface circuit (credit: philibertc)



See the references below for all the details about te circuit.

You can use the 5V output from the stove to power the ESP module, but you will have to put a voltage regulator in between to
get 3v3.

MicroNova configuration
-----------------------

.. code-block:: yaml

    # Example configuration entry
    uart:
      tx_pin: 5
      rx_pin: 4
      baud_rate: 1200
      stop_bits: 2

    micronova:
        enable_rx_pin: 7
        update_interval: 10s
        scan_memory_location: 0x00
        room_temperature:
            memory_address: 0x01
            name: Ambient temperature
            id: ambient_temperature
        thermostat_temperature:
            name: Stove thermostat temperature
        fumes_temperature:
            name: Smoke temperature
        stove_power:
            name: Stove current power
        fan_speed:
            fan_rpm_offset: 240
            name: Fan RPM
            id: fan_rpm
        memory_address_sensor:
            memory_location: 0x20
            memory_address: 0x7d
            name: Memory Adres sensor
            id: mem_adres_sensor
        stove_state:
            memory_address: 0x21
            name: Stove Status
        stove_switch:
            memory_location: 0x80
            memory_address: 0x21
            memory_data_on: 0x01
            memory_data_off: 0x06
            name: Switch stove on/off
        but_temp_up:
            name: Increase thermostat
            memory_location: 0xA0
            memory_address: 0x7D
            memory_data: 0x21
        but_temp_down:
            name: Decrease thermostat


Micronova variables:
~~~~~~~~~~~~~~~~~~~~

- **enable_rx_pin** (**Required**, :ref:`config-pin`): Output pin to be used to switch the line between RX en TX.
- **update_interval** (*Optional*, :ref:`config-time`): The interval that the sensors should be checked.
  Defaults to 60 seconds.
- **scan_memory_location** (*Optional*): When dumping the config, this memory location will be scanned from 0x00 to 0x0F
  for debugging purposes

Sensor variables:
~~~~~~~~~~~~~~~~~

- **room_temperature** (*Optional*): Sensor that reads the stoves ambient room temperature.
- **thermostat_temperature** (*Optional*): The current stove thermostat value.
- **fumes_temperature** (*Optional*): Fumes temperature.
- **stove_power** (*Optional*): Current stove power.
- **fan_speed** (*Optional*): Current fan speed. The raw value from the stove is multiplied by 10 + **fan_rpm_offset**
- **memory_address_sensor** (*Optional*): Can be any **memory_location** / **memory_address** you want to track. Usefull
  when you don't know where the parameter is for your stove is.
- **stove_state** (*Optional*): The current stove state.

All sensors are normal sensors... so all sensor variables are working to.

For all sensors you can set specific **memory_location** and **memory_address** parameters:

- **memory_location** (*Optional*): The memory location where the parameter must be read. For most stoves this is 0x00 for RAM
  or 0x20 for EPROM.
- **memory_address** (*Optional*): The address where the parameter is stored.


Button variables:
~~~~~~~~~~~~~~~~~
To use these buttons, you will need the **thermostat_temperature** sensor.

- **but_temp_up** (*Optional*): Increase the current stove thermostat temperature by 1°C
- **but_temp_up** (*Optional*): Decrease the current stove thermostat temperature by 1°C

For all buttons you can set specific **memory_location**, **memory_address** and **memory_data** parameters:

- **memory_location** (*Optional*): The memory location where the parameter must be written. For most stoves this is 0x80 for RAM
  or 0xA0 for EPROM.
- **memory_address** (*Optional*): The address where the parameter is stored.
- **memory_data** (*Optional*): The data to write.

Switch variables:
~~~~~~~~~~~~~~~~~
- **stove_switch** (*Optional*): Turn the stove on or off. This switch will also reflect the current stove state. 
  If the **stove_state** is "Off" the switch will be off, in all other states, the switch wil be on.

For switches you can set specific **memory_location**, **memory_address**, **memory_data_on** and **memory_data_off** parameters:

- **memory_location** (*Optional*): The memory location where the parameter must be written. For most stoves this is 0x80 for RAM
  or 0xA0 for EPROM.
- **memory_address** (*Optional*): The address where the parameter is stored.
- **memory_data_on** (*Optional*): The data to write when turning the switch on.
- **memory_data_off** (*Optional*): The data to write when turning the switch off.

See Also
--------

- `ridiculouslab micronova <https://www.ridiculouslab.com/arguments/iot/stufa/micronova_en.php>`__
- `philibertc / micronova_controller  <https://github.com/philibertc/micronova_controller/>`__
- `eni23 / micronova-controller  <https://github.com/eni23/micronova-controller>`__
- :ghedit:`Edit`