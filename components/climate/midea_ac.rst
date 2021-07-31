Midea Air Conditioner
=====================

.. seo::
    :description: Instructions for setting up a Midea climate device
    :image: air-conditioner.png

The ``midea_ac`` component creates a Midea air conditioner climate device.

This component requires a auto-loaded ``midea_dongle`` component, that use hardware UART.

.. note::

    This protocol also used by some vendors:

        - `Electrolux <https://www.electrolux.ru/>`_
        - `Qlima <https://www.qlima.com/>`_
        - `Artel <https://www.artelgroup.com/>`_
        - `Carrier <https://www.carrier.com/>`_
        - `Comfee <http://www.comfee-russia.ru/>`_
        - `Inventor <https://www.inventorairconditioner.com/>`_
        - and maybe others

    Example of hardware implementation is `IoT Uni Dongle <https://github.com/dudanov/iot-uni-dongle>`_.

.. code-block:: yaml

    # Example configuration entry

    # Disable logging over UART (required)
    logger:
      baud_rate: 0

    # UART settings for Midea dongle (required)
    uart:
      tx_pin: 1         # hardware dependant
      rx_pin: 3         # hardware dependant
      baud_rate: 9600

    # Optional (if you want modify settings)
    midea_dongle:
      period: 1s
      timeout: 2s
      num_attempts: 3
    
    # Main settings
    climate:
      - platform: midea_ac
        name: "Midea AC"            # Use a unique name.
        autoconf: true              # Autoconfigure most options.
        beeper: true                # Beep on commands.
        visual:                     # Optional. Example of visual settings override.
          min_temperature: 17 °C    # min: 17
          max_temperature: 30 °C    # max: 30
          temperature_step: 0.5 °C  # min: 0.5
        supported_modes:            # All capabilities in this section detected by autoconf.
          - FAN_ONLY                # This capability is always used.
          - HEAT_COOL
          - COOL
          - HEAT
          - DRY
        custom_fan_modes:
          - SILENT
          - TURBO
        supported_presets:          # All capabilities in this section detected by autoconf.
          - ECO
          - BOOST
          - SLEEP                   # This capability is always used.
        custom_presets:             # All capabilities in this section detected by autoconf.
          - FREEZE_PROTECTION
        supported_swing_modes:
          - VERTICAL                # This capability is always used.
          - HORIZONTAL
          - BOTH
        outdoor_temperature:        # Optional. Outdoor temperature sensor (may display incorrect values after long inactivity).
          name: "Temp"
        power_usage:                # Optional. Power usage sensor (only for devices that support this feature).
          name: "Power"
        humidity_setpoint:          # Optional. Indoor humidity sensor (only for devices that support this feature).
          name: "Humidity"

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **midea_dongle_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``midea_dongle`` if you want to use multiple devices.
- **name** (**Required**, string): The name of the climate device.
- **autoconf** (*Optional*, boolean): Get capabilities automatically. Allows you not to manually define most of the capabilities of the appliance.
  Defaults to ``True``.
- **beeper** (*Optional*, boolean): Beeper feedback on command. Defaults to ``False``.
- **supported_modes** (*Optional*, list): List of supported modes. Possible values are: ``HEAT_COOL``, ``COOL``, ``HEAT``, ``DRY``, ``FAN_ONLY``.
- **custom_fan_modes** (*Optional*, list): List of supported custom fan modes. Possible values are: ``SILENT``, ``TURBO``.
- **supported_presets** (*Optional*, list): List of supported presets. Possible values are: ``ECO``, ``BOOST``, ``SLEEP``.
- **custom_presets** (*Optional*, list): List of supported custom presets. Possible values are: ``FREEZE_PROTECTION``.
- **supported_swing_modes** (*Optional*, list): List of supported swing modes. Possible values are: ``VERTICAL``, ``HORIZONTAL``, ``BOTH``.
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
- All other options from :ref:`Climate <config-climate>`.

Configuration variables of midea-dongle component:
**************************************************

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`../uart` if you want
  to use multiple UART buses.
- **transmitter_id** (*Optional*, :ref:`config-id`): Set if you use :doc:`../remote_transmitter` component for IR commands transmit.
- **period** (*Optional*, :ref:`time <config-time>`): Minimal period between requests to the appliance. Defaults to ``1s``.
- **timeout** (*Optional*, :ref:`time <config-time>`): Request response timeout until next request attempt. Defaults to ``2s``.
- **num_attempts** (*Optional*, integer 1-5): Number of request attempts. Defaults to ``3``.


Automations
-----------

.. _midea_ac-follow_me_action:

``midea_ac.follow_me`` Action
*****************************

This action transmit IR FollowMe command telling the air conditioner a more accurate
room temperature value to be used instead of the internal indoor unit sensor.

.. code-block:: yaml

    on_...:
      then:
        - midea_ac.follow_me:
            temperature: !lambda "return x;"
            beeper: false

Configuration variables:

- **temperature** (**Required**, uint8_t, :ref:`templatable <config-templatable>`): Set the
  value of a internal temperature sensor.
- **beeper** (*Optional*, bool, :ref:`templatable <config-templatable>`): set beep on update.
  Defaults to ``False``


.. _midea_ac-display_toggle_action:

``midea_ac.display_toggle`` Action
**********************************

This action toggle ac screen. Works via UART if supported or :doc:`../remote_transmitter`.

.. code-block:: yaml

    on_...:
      then:
        - midea_ac.display_toggle:


.. _midea_ac-swing_step_action:

``midea_ac.swing_step`` Action
******************************

This action adjust the louver by one step. :doc:`../remote_transmitter` required.

.. code-block:: yaml

    on_...:
      then:
        - midea_ac.swing_step:


.. _midea_ac-beeper_on_action:

``midea_ac.beeper_on`` Action
******************************

This action turn on beeper feedback.

.. code-block:: yaml

    on_...:
      then:
        - midea_ac.beeper_on:

.. _midea_ac-beeper_off_action:

``midea_ac.beeper_off`` Action
******************************

This action turn off beeper feedback.

.. code-block:: yaml

    on_...:
      then:
        - midea_ac.beeper_off:


Additional control options using IR commands
--------------------------------------------

It is possible to use the FollowMe function and some other features available only through IR commands.
Below is an example of how to send FollowMe commands with the values of your sensor using the :doc:`../remote_transmitter`
component, as well as control the light of the LED display.

.. code-block:: yaml

    # Example configuration entry

    remote_transmitter:
      pin: GPIO13                 # For iot-uni-stick
      carrier_duty_percent: 100%  # 50% for IR LED, 100% for direct connect to TSOP IR receiver output.

    midea_dongle:
      transmitter_id:             # Add this option to use IR transmitter.

    sensor:
      - platform: homeassistant
        internal: true
        entity_id: sensor.room_sensor # Sensor from HASS
        filters:
          - throttle: 10s
          - heartbeat: 2min       # Maximum interval between updates.
          - debounce: 1s
        on_value:
          - midea_ac.follow_me:
              temperature: !lambda "return x;"
              beeper: false       # Optional. Beep on update.

    # template momentary switches for sending display control command and swing step actions
    switch:
      - platform: template
        name: "Display Toggle"
        icon: "mdi:theme-light-dark"
        turn_on_action:
          - midea_ac.display_toggle:
      - platform: template
        name: "Swing Step"
        icon: "mdi:tailwind"
        turn_on_action:
          - midea_ac.swing_step:


Example of Beeper Control Using a Switch
----------------------------------------

.. code-block:: yaml

    switch:
      - platform: template
        name: "Beeper"
        icon: "mdi:volume-source"
        optimistic: true
        turn_on_action:
          - midea_ac.beeper_on:
        turn_off_action:
          - midea_ac.beeper_off:

Acknowledgments:
----------------

Thanks to the following people for their contributions to reverse engineering the UART protocol and source code in the following repositories:

* `Mac Zhou <https://github.com/mac-zhou/midea-msmart>`_
* `NeoAcheron <https://github.com/NeoAcheron/midea-ac-py>`_
* `Rene Klootwijk <https://github.com/reneklootwijk/midea-uart>`_

Special thanks to the project `IRremoteESP8266 <https://github.com/crankyoldgit/IRremoteESP8266>`_ for describing the IR protocol.

See Also
--------

- :doc:`/components/climate/index`
- :apiref:`climate/midea_ac.h`
- :ghedit:`Edit`
