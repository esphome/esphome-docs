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
      enable_rx_pin: 4
      update_interval: 20s

    text_sensor:
      - platform: micronova
        stove_state:
          name: Stove status

    number:
      - platform: micronova
        thermostat_temperature:
          name: Thermostat temperature

    sensor:
      - platform: micronova
        room_temperature:
          name: Room temperature
        fumes_temperature:
          name: Fumes temperature
        water_temperature:
          name: Water temperature
          # every sensor can specify memory parameters
          memory_location: 0x00
          memory_address: 0x3B
        water_pressure:
          name: Water pressure
        stove_power:
          name: Stove power level
        fan_speed:
          fan_rpm_offset: 240
          name: Fan RPM
        memory_address_sensor:
          memory_location: 0x20
          memory_address: 0x7d
          name: Custom Address sensor

    switch:
      - platform: micronova
        stove:
          name: Stove on/off switch

    button:
      - platform: micronova
        temperature_up:
          name: Thermostat Up
        temperature_down:
          name: Thermostat Down


Micronova variables:
~~~~~~~~~~~~~~~~~~~~

- **enable_rx_pin** (**Required**, :ref:`config-pin`): Output pin to be used to switch the line between RX en TX.
- **update_interval** (*Optional*, :ref:`config-time`): The interval that the sensors should be checked.
  Defaults to 60 seconds.

.. note::

    For most Micronova boards the default **memory_location** and **memory_address** parameters will work so you should
    not specify them. However your Micronova boad may require you to specify alternate values. So every (text)sensor, button,
    switch or number accepts these parameters:

    - **memory_location** (*Optional*): The memory location where the parameter must be read. For most stoves this is 0x00 for RAM
      or 0x20 for EPROM.
    - **memory_address** (*Optional*): The address where the parameter is stored.


Text Sensor variables:
~~~~~~~~~~~~~~~~~
- **stove_state** (*Optional*): The current stove state.
- All other options from :ref:`Text Sensor <config-text_sensor>`.

Sensor variables:
~~~~~~~~~~~~~~~~~
- **room_temperature** (*Optional*): Sensor that reads the stoves ambient room temperature.
- **thermostat_temperature** (*Optional*): The current stove thermostat value.
- **fumes_temperature** (*Optional*): Fumes temperature.
- **stove_power** (*Optional*): Current stove power.
- **fan_speed** (*Optional*): Current fan speed. The raw value from the stove is multiplied by 10 + **fan_rpm_offset**
- **memory_address_sensor** (*Optional*): Can be any **memory_location** / **memory_address** you want to track. Usefull
  when you don't know where the parameter is for your stove is.
- All other options from :ref:`Sensor <config-sensor>`.


Number variables:
~~~~~~~~~~~~~~~~~
- **thermostat_temperature** (*Optional*): Number that holds the current stove thermostat value.
- All other options from :ref:`Number <config-number>`.

.. note::

    Besides **memory_location** and **memory_address** you can specify a specific **memory_write_location** parameter.
    This parameter is a hex value for the **memory_location** where the new thermostat value must be written.

    - **memory_write_location** (*Optional*): The **memory_location** where to write the new thermostat value.

Button variables:
~~~~~~~~~~~~~~~~~
To use these buttons, you will need the **thermostat_temperature** sensor.

- **temperature_up** (*Optional*): Increase the current stove thermostat temperature by 1°C
- **temperature_down** (*Optional*): Decrease the current stove thermostat temperature by 1°C
- All other options from :ref:`Button <config-button>`.

.. note::

    Besides **memory_location** and **memory_address** you can specify a specific **memory_data** parameter.
    This parameter is the hex value to be written to the **memory_location** and **memory_address** location when pressing the button.

    - **memory_data** (*Optional*): The hex value to be written to the **memory_location** and **memory_address**.

Switch variables:
~~~~~~~~~~~~~~~~~
- **stove** (*Optional*): Turn the stove on or off. This switch will also reflect the current stove state. 
  If the **stove_state** is "Off" the switch will be off, in all other states, the switch wil be on.
- All other options from :ref:`Switch <config-switch>`.

.. note::

    Besides **memory_location** and **memory_address** you can specify specific **memory_data_on** and **memory_data_off** parameters. 
    These parameters contain the hex value to be written to the **memory_location** and **memory_address** when the switch 
    turns on or off.

    - **memory_data_on** (*Optional*): The data to write when turning the switch on.
    - **memory_data_off** (*Optional*): The data to write when turning the switch off.

See Also
--------

- `ridiculouslab micronova <https://www.ridiculouslab.com/arguments/iot/stufa/micronova_en.php>`__
- `philibertc / micronova_controller  <https://github.com/philibertc/micronova_controller/>`__
- `eni23 / micronova-controller  <https://github.com/eni23/micronova-controller>`__
- :ghedit:`Edit`
