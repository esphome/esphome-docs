Fluval BLE LED
==============

.. seo::
    :description: Instructions for setting up Fluval BLE LED devices in ESPHome.
    :image: led-on.svg

The ``fluval_ble_led`` component allows you to connect to your Smart Fluval LED.
Up to 3 devices can be connected with a single ESP32. 

.. warning::

  Due to limitations of Bluetooth Low Energy, only one device can connect to a 
  Fluval LED at a time. If you connect this component to the Fluval LED, 
  you are no longer able to connect with the Fluval app. 
  In order to control your Fluval LED with the Fluval app, disconnect the component 
  first, for example by powering down the ESP32.

.. note::

    Fluval LED devices support 3 different modes: manual, auto and pro.
    This component supports reading the current mode and changing the mode.

    Manually switching the LED on and off as well as reading and setting the channel
    values only works in manual mode. 

Supported devices
-----------------

The following devices are supported independent of size (including Nano):

- AquaSky 2.0 (4 channels)
- Plant 3.0 (5 channels)
- Marine 3.0 (5 channels)

Essentially all devices which usually are controlled by the Fluval App.

Setup of prerequisites
----------------------

The ``fluval_ble_led`` component requires a ``ble_client`` to communicate with the
LED devices, which in turn requires the ``esp32_ble_tracker``  component in order
to discover client devices.

.. code-block:: yaml

    esp32_ble_tracker:

    ble_client:
      - mac_address: 44:A6:E5:00:E8:01
        id: ble_fluval1
      - mac_address: 44:A6:E5:00:E8:02
        id: ble_fluval2
      - mac_address: 44:A6:E5:00:E8:03
        id: ble_fluval3

This example shows a configuration with the maximum of 3 Fluval LEDs configured.

.. note::

    To find the required mac_address, use a tool like nRF Connect on your smartphone or
    check the documentation. :ref:`Setting up devices <esp32_ble_tracker-setting_up_devices>` 
    on how to scan for devices using the ``esp32_ble_tracker``.

In addition to the communication, Fluval LED devices require a time synchronization.
For this purpose, a ``time`` source needs to be set up. 
In this case, using the homeassistant timesource:


.. code-block:: yaml

    time:
      - platform: homeassistant
        id: ha_time 

Component
---------

Now the ``fluval_ble_led`` component is added to the configuration:

.. code-block:: yaml

    fluval_ble_led:
      - ble_client_id: ble_fluval1
        time_id: ha_time
        number_of_channels: 5
        id: fluval_1

      - ble_client_id: ble_fluval2
        time_id: ha_time
        number_of_channels: 4
        id: fluval_2

      - ble_client_id: ble_fluval3
        time_id: ha_time
        number_of_channels: 4
        id: fluval_3

Configuration variables:

The configuration is mainly giving the previously created ``ble_client`` components as refrence
for communication, as well as the time source and the number of channels the Fluval LED device has.

- **ble_client_id** (*Required*, :ref:`config-id`): Specify the ``ble_client`` to use.
- **time_id** (*Required*, :ref:`config-time`): Specify the ``time`` source to use.
- **number_of_channels** (*Required*, int): The number of channels the Fluval LED device supports. This can be either 4 or 5.
- **id** (*Required*, :ref:`config-id`): ID of the Fluval LED. Will be used in sensors, switches etc.

Button
------

Buttons can be used to switch between the 3 modes of the Fluval LED: 
- manual
- auto
- pro

.. code-block:: yaml

    button:  
      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        mode: "MANUAL"
        name: "Switch to manual"

      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        mode: "AUTO"
        name: "Switch to auto"

      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        mode: "PRO"
        name: "Switch to pro"

Configuration variables:

- **fluval_ble_led_id** (*Required*, :ref:`config-id`): Specify the ``fluval_ble_led`` to use.
- **mode** (*Required*, string): Select the mode. Either "MANUAL", "AUTO" or "PRO"
- **name** (**Required**, string): The name for the button.

Switch
------

The switch can be used to turn the Fluval LED on or off. This turns of the light, not the device itself.

.. code-block:: yaml

    switch:
      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        name: "Tank 1 light"

Configuration variables:

- **fluval_ble_led_id** (*Required*, :ref:`config-id`): Specify the ``fluval_ble_led`` to use.
- **name** (**Required**, string): The name for the switch.

Text sensor
-----------

This sensor displays the current mode of the Fluval LED device. It allows mapping of the different
modes to custom text, for example to accomodate different languages.

.. code-block:: yaml

    text_sensor:
      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        mapping_manual: "Manuell"
        mapping_auto: "Automatisch"
        mapping_pro: "Professionell"
        name: "Tank 1 mode"

Configuration variables:

- **fluval_ble_led_id** (*Required*, :ref:`config-id`): Specify the ``fluval_ble_led`` to use.
- **mapping_manual** (*Optional*, string): Specify the text when in manual mode.
- **mapping_auto** (*Optional*, string): Specify the text when in auto mode.
- **mapping_pro** (*Optional*, string): Specify the text when in pro mode.
- **name** (**Required**, string): The name for the text sensor.

Sensor
------

Regular sensors can be added to display the current level of each channel. These levels range from 0 to 1000.

.. code-block:: yaml

    sensor:    
      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        channel: 1       
        zero_if_off: true
        name: "Rose"

      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        channel: 2       
        zero_if_off: true 
        name: "Blue"  

      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        channel: 3       
        zero_if_off: true 
        name: "Cold white"  

      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        channel: 4       
        zero_if_off: true 
        name: "Pure white"

      - platform: fluval_ble_led
        fluval_ble_led_id: fluval_1
        channel: 5       
        zero_if_off: true 
        name: "warm white"

Configuration variables:

- **fluval_ble_led_id** (*Required*, :ref:`config-id`): Specify the ``fluval_ble_led`` to use.
- **channel** (*Required*, int): Channel number this sensor is using.
- **zero_if_off** (*Optional*, boolean): If the channel could not be read, output 0 instead of "unknown"
- **name** (**Required**, string): The name for the sensor.

Number
------

Similar to the sensors, numbers are linked to channels and display their status. They can be manipulated
though to change the channel value and thus the light. 

.. code-block:: yaml

    number:
    - platform: fluval_ble_led
      fluval_ble_led_id: fluval_1
      name: "Rose"
      channel: 1
      zero_if_off: true

    - platform: fluval_ble_led
      fluval_ble_led_id: fluval_1
      name: "Blue"
      channel: 2
      zero_if_off: true

    - platform: fluval_ble_led
      fluval_ble_led_id: fluval_1
      name: "Cold white"
      channel: 3
      zero_if_off: true

    - platform: fluval_ble_led
      fluval_ble_led_id: fluval_1
      name: "Pure White"
      channel: 4
      zero_if_off: true

    - platform: fluval_ble_led
      fluval_ble_led_id: fluval_1
      name: "Warm White"
      channel: 5
      max_value: 500
      min_value: 200
      step: 50
      zero_if_off: true

Configuration variables:

- **fluval_ble_led_id** (*Required*, :ref:`config-id`): Specify the ``fluval_ble_led`` to use.
- **channel** (*Required*, int): Channel number this number is using.
- **max_value** (*Optional*, int): Maximum value that this number can send to the channel. Can not be higher than 1000. The default is 1000.
- **min_value** (*Optional*, int): Minimum value that this number can send to the channel. Can not be lower than 0. The default is 0.
- **step** (*Optional*, int): In which steps the value will change. The default is 100.
- **zero_if_off** (*Optional*, boolean): If the channel could not be read, output 0 instead of "unknown"
- **name** (**Required**, string): The name for the number.

See Also
--------

- :ghedit:`Edit`
