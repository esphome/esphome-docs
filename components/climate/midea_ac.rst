Midea Air Conditioner
=====================

.. seo::
    :description: Instructions for setting up a Midea climate device
    :image: air-conditioner.png

The ``midea_ac`` component creates a Midea air conditioner climate device.

This component requires a auto-loaded ``midea-dongle`` component, that use hardware UART.

.. note::

    This protocol also used by some vendors:

        - `Electrolux <https://www.electrolux.ru/>`_
        - `Qlima <https://www.qlima.com/>`_
        - `Artel <https://www.artelgroup.com/>`_
        - `Carrier <https://www.carrier.com/>`_
        - `Comfee <http://www.comfee-russia.ru/>`_
        - `Inventor <https://www.inventorairconditioner.com/>`_
        - and maybe others

    Example of hardware implementation is `Midea Open Dongle <https://github.com/dudanov/midea-open-dongle>`_ in free `KiCad <https://kicad-pcb.org>`_ format.

.. code-block:: yaml

    # Example configuration entry

    # Disable logging over UART (required)
    logger:
      baud_rate: 0

    # UART settings for Midea dongle (required)
    uart:
      tx_pin: 1   # hardware dependant
      rx_pin: 3   # hardware dependant
      baud_rate: 9600

    # Optional (if you want modify settings)
    midea_dongle:
      strength_icon: true   # for devices that supporting indication of several levels of signal quality
    
    # Main settings
    climate:
      - platform: midea_ac
        name: "Midea AC #1"   # use a unique name
        visual:
          min_temperature: 17 °C    # min: 17
          max_temperature: 30 °C    # max: 30
          temperature_step: 0.5 °C  # min: 0.5
        beeper: true  # beep on commands
        custom_fan_modes:
          - SILENT
          - TURBO
        preset_eco: true
        preset_sleep: true
        preset_boost: true
        custom_presets:
          - FREEZE_PROTECTION
        swing_horizontal: true
        swing_both: true
        outdoor_temperature:  # create outdoor unit temperature sensor (may display incorrect values after long inactivity)
          name: "Temp"        # sensor unique name
        power_usage:          # create power usage sensor (only for devices that support this feature)
          name: "Power"       # sensor unique name
        humidity_setpoint:    # create indoor humidity sensor
          name: "Hum"         # sensor unique name

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **midea_dongle_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``midea_dongle`` if you want to use multiple devices.
- **name** (**Required**, string): The name of the climate device.
- **outdoor_temperature** (*Optional*): The information for the outdoor temperature
  sensor.

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.
- **power_usage** (*Optional*): The information for the current power consumption
  sensor.

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.
- **humidity_setpoint** (*Optional*): The information for the humidity indoor
  sensor (experimental).

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.
- **beeper** (*Optional*, boolean): Beeper feedback on command. Defaults to ``False``.
- **custom_fan_modes** (*Optional*, list): List of supported custom fan modes. Possible values are: SILENT, TURBO.
- **preset_eco** (*Optional*, boolean): ECO preset support. Defaults to ``False``.
- **preset_sleep** (*Optional*, boolean): SLEEP preset support. Defaults to ``False``.
- **preset_boost** (*Optional*, boolean): BOOST preset support. Defaults to ``False``.
- **custom_presets** (*Optional*, list): List of supported custom presets. Possible values are: FREEZE_PROTECTION.
- **swing_horizontal** (*Optional*, boolean): Enable **swing horizontal** option. Defaults to ``False``.
- **swing_both** (*Optional*, boolean): Enable **swing both** option. Defaults to ``False``.
- All other options from :ref:`Climate <config-climate>`.

Configuration variables of midea-dongle component:
**************************************************

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`../uart` if you want
  to use multiple UART buses.
- **strength_icon** (*Optional*, boolean): Set if your device have signal strength icon
  and you want to use this feature. By default, on connected state, icon show maximum signal quality. Defaults to ``False``.


Additional control options using IR commands
--------------------------------------------

It is possible to use the FollowMe function and some other features available only through IR commands.
Below is an example of how to send FollowMe commands with the values of your sensor using the :doc:`../remote_transmitter`
component, as well as control the light of the LED display.

.. code-block:: yaml

    # Example configuration entry

    remote_transmitter:
      pin: GPIO13                 # for midea-open-dongle hardware stick
      carrier_duty_percent: 100%  # 50% for IR LED, 100% for direct connect to TSOP IR receiver output

    sensor:
      - platform: homeassistant
        id: fm_sensor
        entity_id: sensor.room_sensor # sensor from HASS
        filters:
          - throttle: 10s
          - heartbeat: 2min # minimum interval of FM commands
          - debounce: 1s
        on_value:
          - remote_transmitter.transmit_midea_follow_me:
              beeper: false   # may beep on every FM command (or not?)
              temperature: !lambda "return x;"

    # template momentary switch for sending display control command
    switch:
      - platform: template
        name: "Toggle Display"
        icon: "mdi:theme-light-dark"
        id: mlight
        turn_on_action:
          - remote_transmitter.transmit_midea_toggle_light:
          - switch.turn_off: mlight


Acknowledgments:
----------------

Thanks to the following people for their contributions to reverse engineering the UART protocol and source code in the following repositories:

* `Mac Zhou <https://github.com/mac-zhou/midea-msmart>`_
* `NeoAcheron <https://github.com/NeoAcheron/midea-ac-py>`_
* `Rene Klootwijk <https://github.com/reneklootwijk/node-mideahvac>`_

Special thanks to the project `IRremoteESP8266 <https://github.com/crankyoldgit/IRremoteESP8266>`_ for describing the IR protocol.

See Also
--------

- :doc:`/components/climate/index`
- :apiref:`climate/midea_ac.h`
- :ghedit:`Edit`
