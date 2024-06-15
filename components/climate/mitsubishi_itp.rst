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
      - platform: mitsubishi_ipt
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
- **temperature_sources** (*Optional*): A list of sensor :ref:`config-id` s reporting temperatures **in Celsius**; used to populate the temperature source select component.
- **supported_modes** (*Optional*): List of modes supported by this climate device.  A combination of

  - ``OFF`` - The device is manually set to off, the device is inactive.
  - ``HEAT`` - The device is set to heat to reach a target temperature.
  - ``COOL`` - The device is set to cool to reach a target temperature.
  - ``HEAT_COOL`` - The device should heat/cool to maintain a target temperature.
  - ``FAN_ONLY`` - The device only has the fan enabled, no heating or cooling is taking place.
  - ``DRY`` - The device is set to dry/humidity mode.
- **supported_fan_modes** (*Optional*): List of fan modes supported, defaults to: [``AUTO``, ``QUIET``, ``LOW``, ``MEDIUM``, ``HIGH``].
- **custom_fan_modes** (*Optional*): List of additional supported fan modes, defaults to ``VERYHIGH``.
- **selects** (*Optional*): Custom configuration for any of the select components used by this device (see below).
- **sensors** (*Optional*): Custom configuration for any of the sensors provided by this device (see below).

Thermostat Support
------------------------

An MHK2 thermostat can be connected via a second UART component.  Communication from the thermostat will be forwarded to the equipment, allowing both the thermostat and Home Assistant to be used for control.  The thermostat can also be used as a temperature source when connected.

Active Mode
------------------------

The device has an "Active Mode" switch that defaults to ``on`` for normal operation.  If switched to ``off``, this component will not generate any UART packets of its own and will simply forward and record packets being sent by an attached thermostat.  This is useful for a "read only" implementation where control from Home Assistant isn't desired but data collection and recording is.

Temerature Sources
------------------------
The Mitsubishi ITP component can use other ESPHome sensors to report current temperature (*in Celsius!*) to the heat pump.  **IMPORTANT:** This component does not poll the sensors explicitly, but rather subscribes to update events on the sensors.  If no updates have been received for 7 minutes, the equipment will be switched back to its internal temperature sensor.  This means that even if the temperature hasn't changed, the sensors need to publish updates.  This may require the use of e.g. ``force_update: true`` to make sure updates are sent regularly.

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

    climate:
      - platform: mitsubishi_ipt
        uart_heatpump: hp_uart
        temperature_sources:
          - home_assistant_temperature


An automation in Home Assistant can then be configured with an action like the following to report a temperature to the device:

.. code-block:: yaml

    action:
      - service: esphome.office_heatpump_report_temperature
        data:
          current_temperature_C: "{{float(states('sensor.office_temperature'))}}"


Built-in Sensors
------------------------
The Mitsubishi ITP device has several built in sensors whose default configuration can be overridden using the normal sensor variables (see: :ref:`config-sensor`).  These sensors are disabled by default in Home Assistant but can be enabled if desired.

.. note::

    Not all sensors are available on all equipment.

Current built-in sensors include: 

- **thermostat_temperature**: If a thermostat is connected, reports the last temperature received from the thermostat.
- **compressor_frequency**: Frequency in Hz reported by a variable speed compressor.
- **actual_fan**: The actual speed the fan is running at (may differ from set-speed once set-point has been reached or during preheating).
- **service_filter**: Reports if filter needs to be replaced.
- **defrost**: Reports if system is in defrost
- **hot_adjust**: Reports if system is preheating
- **standby**: Reports if system is in standby
- **error_code**: Reports error codes (if any)

Select Configuration
------------------------
The Mitsubishi ITP device has several select components built in whose default configuration can be overridden using the normal select variables (see: :ref:`config-select`).  Current built-in select components include: 

- ``vane_position_select``
- ``horizontal_vane_position_select``
- ``temperature_source_select``


See Also
--------

- :doc:`/components/climate/index`
- :ghedit:`Edit`
