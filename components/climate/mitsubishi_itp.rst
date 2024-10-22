Mitsubishi ITP
=====================

.. seo::
    :description: Instructions for setting up an IT Protocol Mitsubishi heatpump via UART
    :image: air-conditioner.svg

The ``mitsubishi_itp`` component creates a climate device for controlling a Mitsubishi heatpump with the IT Protocol connected via UART.  Optionally also supports connecting an MHK2 thermostat.

.. note::

    This component requires connecting to the heatpump via UART.  Additional documentation, including hardware setup is available `here <https://muart-group.github.io/>`_.

.. code-block:: yaml

    # Example minimal configuration entry

    climate:
      - platform: mitsubishi_itp
        name: "Climate"
        uart_heatpump: hp_uart

    uart:
      - id: hp_uart
        baud_rate: 2400 # Some devices may require 9600
        parity: EVEN
        rx_pin:
            number: GPIO7
        tx_pin:
            number: GPIO6

Configuration variables:
------------------------

- **uart_heatpump** (**Required**, :ref:`config-id`): Id of the UART component that is connected to the heat pump.
- **uart_thermostat** (*Optional*, :ref:`config-id`): Id of the UART component that is connected to the MHK2 thermostat (if present).
- **name** (*Optional*, string): The name for this heat pump.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **update_interval** (*Optional*, :ref:`config-time`): How long to wait between polling the equipment for state and updating Home Assistant.
- **supported_modes** (*Optional*): List of modes supported by this climate device.  A combination of

  - ``OFF`` - The device is manually set to off, the device is inactive.
  - ``HEAT`` - The device is set to heat to reach a target temperature.
  - ``COOL`` - The device is set to cool to reach a target temperature.
  - ``HEAT_COOL`` - The device should heat/cool to maintain a target temperature.
  - ``FAN_ONLY`` - The device only has the fan enabled, no heating or cooling is taking place.
  - ``DRY`` - The device is set to dry/humidity mode.
- **supported_fan_modes** (*Optional*): List of fan modes supported, defaults to: [``AUTO``, ``QUIET``, ``LOW``, ``MEDIUM``, ``HIGH``].
- **custom_fan_modes** (*Optional*): List of additional supported fan modes, defaults to ``VERYHIGH``.

Thermostat Support
------------------------

An MHK2 thermostat can be connected via a second UART component.  Communication from the thermostat will be forwarded to the equipment, allowing both the thermostat and Home Assistant to be used for control.  The thermostat can also be used as a temperature source when connected.  Don't forget to add the `uart_thermostat` variable to the `climate` component (see above).

.. _supported_basic_sensors:

Supported Basic Sensors
------------------------

.. note::

    Not all sensors are available on all equipment.  SEE :ref:`NOTES <sensor_notes>`.

The Mitsubishi ITP device has several supported sensors that can be added.  Each sensor must be explicitly added in the config file, and supports the usual sensor options (see: :ref:`config-sensor`).  The configuration snippet below contains all the basic sensors and a brief description of each.

.. code-block:: yaml

    binary_sensor:
      - platform: mitsubishi_itp
        defrost:
          # Reports if system is in defrost
          name: "Defost"
        filter_status:
          # Reports if filter needs to be replaced (false = OK)
          name: "Filter Status"
        isee_status:
          # Reports if i-see is enabled
          name: "i-see Status"
        preheat:
          # Reports if system is preheating
          name: "Preheat"
        standby:
          # Reports if system is in standby
          name: "Standby"

    sensor:
      - platform: mitsubishi_itp
        compressor_frequency:
          # Frequency in Hz of compressor (only some equipment)
          name: "Compressor Frequency"
        outdoor_temperature:
          # Outdoor temperature as reported by equipment
          name: "Outdoor Temperature"

        # Only available if a thermostat is connected
        thermostat_humidity:
          # Humidity reported by thermostat (only with enhanced_mhk)
          name: "Thermostat Humidity"
        thermostat_temperature:
          # Temperature reported by thermostat
          name: "Thermostat Temperature"

    text_sensor:
      - platform: mitsubishi_itp
        actual_fan:
          # Actual current fan speed (vs. set speed)
          name: "Actual Fan"
        error_code:
          # Reports diagnostic error code
          name: "Error Code"
        
        # Only available if a thermostat is connected
        thermostat_battery:
          # Thermostat battery status (only with enhanced_mhk)
          name: "Thermostat Battery"

.. _sensor_notes:

Sensor Notes
------------------------
- **outdoor_temperature**: The reported data from equipment seems to be inconsistent for outdoor temperature, so this should not be conisdered a reliable temperature source.
- **actual_fan**: When the unit has reached its set-point, or during preheating, the fan may run at a speed other than the requested speed.  This sensor shows the "actual" current speed.

Vane Control
------------------------
On units with vertical or horizontal vane control, the following components can be added to the configuration to enable control.  These can be additionally configured via :ref:`config-select`.

.. code-block:: yaml

    select:
      - platform: mitsubishi_itp
        vane_position:
          name: "Vane Position"
        horizontal_vane_position:
          name: "H. Vane Position"

Filter Reset
------------------------
A button can be added to reset the filter change status:

.. code-block:: yaml

    button:
    - platform: mitsubishi_itp
      filter_reset_button:
        name: "Filter Reset"

Temperature Sources
------------------------
The Mitsubishi ITP component can use other ESPHome sensors to report current temperature (*in Celsius!*) to the heat pump.  **IMPORTANT:** This component does not poll the sensors explicitly, but rather subscribes to update events on the sensors.  If no updates have been received for 7 minutes, the equipment will be switched back to its internal temperature sensor.  This means that even if the temperature hasn't changed, the sensors need to publish updates.  This may require the use of e.g. ``force_update: true`` to make sure updates are sent regularly.

To enable the Temperature Source select component, add it to the configuration:

.. code-block:: yaml

    select:
      - platform: mitsubishi_itp
        temperature_source:
          name: "Temperature Source"
          sources:
            # List of temperature sensor ids
            # 'Thermostat' will be automatically included if configured

One particularly useful way to get additional temperature data is by having Home Assistant send the data to the device via a service.  Here is an example configuration for that scenario:

.. code-block:: yaml

    esphome:
      name: office-heatpump

    api:
      services:
        - service: report_temperature
            variables:
              current_temperature_C: float
            then:
              - sensor.template.publish:
                  id: home_assistant_temperature
                  state: !lambda "return current_temperature_C;"

    sensor:
      - platform: template
        id: home_assistant_temperature
        internal: true
        name: "Home Assistant"
        update_interval: never # Only updated by service

    select:
        - platform: mitsubishi_itp
          temperature_source:
            name: "Temperature Source"
            sources:
              - home_assistant_temperature

    climate:
      - platform: mitsubishi_itp
        name: "Climate"
        uart_heatpump: hp_uart


An automation in Home Assistant can then be configured with an action like the following to report a temperature to the device:

.. code-block:: yaml

    action:
      - service: esphome.office_heatpump_report_temperature
        data:
          current_temperature_C: "{{float(states('sensor.office_temperature'))}}"

Enhanced MHK Mode
------------------------
When connected to an MHK2 thermostat, Mitsubishi ITP can attempt to emulate a Mitsubishi Kumo device to enable additional functionality.  **This mode is experimental** and may not be stable or well-supported on all equipment configurations.  To enable this mode, set `enhanced_mhk` to true; this also requires a time source be defined.

.. code-block:: yaml

    time:
      - platform: homeassistant
        id: homeassistant_time
        timezone: America/Los_Angeles

    climate:
      - platform: mitsubishi_itp
        name: "Climate"
        uart_heatpump: hp_uart
        enhanced_mhk: true

This mode will:

- Auto-set the clock on the thermostat
- Retreive humidity and battery data from the thermostat (see :ref:`above<supported_basic_sensors>`)

See Also
--------

- :doc:`/components/climate/index`
- `mUART Group Documentation <https://muart-group.github.io/>`_
- :ghedit:`Edit`
