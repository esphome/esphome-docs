Total Energy Consumption Per Day
================================

Some components (like the :doc:`Sonoff POW R1 </esphomeyaml/components/sensor/hlw8012>`,
:doc:`Sonoff POW R2 </esphomeyaml/components/sensor/cse7766>`, :doc:`self-made power meter <power_meter>`, ...)
can provide the power usage in watts - so the amount of energy currently consumed per unit of time.

However, sometimes it's desired to have a sensor that shows the total energy consumption per day in watt **hours**.

Fortunately, you can use existing components inside esphomeyaml/lib to create such a sensor. The configuration
is split up into three main components:

- A :doc:`template sensor </esphomeyaml/components/sensor/template>`
- The power meter (for example :doc:`power_meter`)
- A :doc:`time component </esphomeyaml/components/time>`

The template sensor here is basically just a stub. It doesn't report any values itself (`return {}`), and
all state updates will be supplied from outside using `publish_state`. We're giving it a ``name`` so that
it shows up in the frontend, an ``id`` so that we can address it in :ref:`lambdas <config-lambda>`.
Additionally, a ``unit_of_measurement`` is set (so that the value shows up with a unit in the front end)
and the default ``filters`` are disabled (see :ref:`sensor-default_filter`).

The power meter (here with a generic platform ``<THE_PLATFORM>``), observes the power values as it would normally.
Each time the pulse counter receives a value, a lambda is triggered that houses most of the logic. In this lambda,
we have a static variable ``last_update`` which we use to get the relative time in hours since the last call of our
lambda. Then we just multiply the value ``x`` from the power meter by the relative time (formula ``Energy = Power * time``).
Lastly, that value is published to the template sensor.

And the ``time`` component is in charge of resetting the total energy every day at midnight (you can of course
change the time for your needs).

.. code:: yaml

    sensor:
    # This is the sensor displaying total energy consumed.
    - platform: template
      lambda: 'return {};'
      update_interval: never
      name: "Total Daily Energy Usage"
      id: total_energy
      unit_of_measurement: kWh
      # Disable filters
      filters:
      accuracy_decimals: 2

    # This is the power meter which outputs values
    - platform: <THE_PLATFORM>
      # ...
      # Disable default filters
      filters:
      on_value:
        lambda: |-
          static uint32_t last_update = 0;
          if (last_update == 0)
            id(total_energy).publish_state(0);
          // the time since the last update in hours
          float delta_time = (millis() - last_update) / 1000.0 / 60.0 / 60.0;
          last_update = millis();

          // x is the power in kW.
          // the energy consumed in this interval in kWh (E = P * t)
          float consumed_energy_kwh = x * delta_time;
          id(total_energy).publish_state(id(total_energy).state + consumed_energy_kwh);

    time:
    - platform: sntp
      id: time
      on_time:
        # Reset total energy at midnight
        seconds: 0
        minutes: 0
        hours: 0
        then:
          lambda: |-
            id(total_energy).publish_state(0);

Configuration for Pulse-Counter based Power Meters
--------------------------------------------------

.. code:: yaml

    sensor:
    # This is the sensor displaying total energy consumed.
    - platform: template
      lambda: 'return {};'
      update_interval: never
      name: "Total Daily Energy Usage"
      id: total_energy
      unit_of_measurement: kWh
      # Disable filters
      filters:
      accuracy_decimals: 2

    # This is the power meter which outputs values
    - platform: pulse_counter
      pin: GPIO12
      unit_of_measurement: 'kW'
      name: 'Power Meter'
      filters:
        - multiply: 0.06
      on_value:
        lambda: |-
          static uint32_t last_update = 0;
          if (last_update == 0)
            id(total_energy).publish_state(0);
          // the time since the last update in hours
          float delta_time = (millis() - last_update) / 1000.0 / 60.0 / 60.0;
          last_update = millis();

          // x is the power in kW.
          // the energy consumed in this interval in kWh (E = P * t)
          float consumed_energy_kwh = x * delta_time;
          id(total_energy).publish_state(id(total_energy).state + consumed_energy_kwh);

    time:
    - platform: sntp
      id: time
      on_time:
        # Reset total energy at midnight
        seconds: 0
        minutes: 0
        hours: 0
        then:
          lambda: |-
            id(total_energy).publish_state(0);

Configuration for Sonoff POW R1
-------------------------------

.. code:: yaml

    sensor:
    # This is the sensor displaying total energy consumed.
    - platform: template
      lambda: 'return {};'
      update_interval: never
      name: "Total Daily Energy Usage"
      id: total_energy
      unit_of_measurement: kWh
      # Disable filters
      filters:
      accuracy_decimals: 2

    # This is the power meter which outputs values
    - platform: hlw8012
      sel_pin: 5
      cf_pin: 14
      cf1_pin: 13
      # current, voltage, ...
      power:
        name: "HLW8012 Power"
        on_value:
          lambda: |-
            static uint32_t last_update = 0;
            if (last_update == 0)
              id(total_energy).publish_state(0);
            // the time since the last update in hours
            float delta_time = (millis() - last_update) / 1000.0 / 60.0 / 60.0;
            last_update = millis();

            // x is the power in W.
            // the energy consumed in this interval in kWh (E = P * t)
            float consumed_energy_kwh = x * delta_time / 1000.0;
            id(total_energy).publish_state(id(total_energy).state + consumed_energy_kwh);

    time:
    - platform: sntp
      id: time
      on_time:
        # Reset total energy at midnight
        seconds: 0
        minutes: 0
        hours: 0
        then:
          lambda: |-
            id(total_energy).publish_state(0);

Configuration for Sonoff POW R2
-------------------------------

.. code:: yaml

    logger:
      baud_rate: 0

    uart:
      rx_pin: RX
      baud_rate: 4800

    sensor:
    # This is the sensor displaying total energy consumed.
    - platform: template
      lambda: 'return {};'
      update_interval: never
      name: "Total Daily Energy Usage"
      id: total_energy
      unit_of_measurement: kWh
      # Disable filters
      filters:
      accuracy_decimals: 2

    # This is the power meter which outputs values
    - platform: cse7766
      # current, voltage, ...
      power:
        name: "CSE7766 Power"
        on_value:
          lambda: |-
            static uint32_t last_update = 0;
            if (last_update == 0)
              id(total_energy).publish_state(0);
            // the time since the last update in hours
            float delta_time = (millis() - last_update) / 1000.0 / 60.0 / 60.0;
            last_update = millis();

            // x is the power in W.
            // the energy consumed in this interval in kWh (E = P * t)
            float consumed_energy_kwh = x * delta_time / 1000.0;
            id(total_energy).publish_state(id(total_energy).state + consumed_energy_kwh);

    time:
    - platform: sntp
      id: time
      on_time:
        # Reset total energy at midnight
        seconds: 0
        minutes: 0
        hours: 0
        then:
          lambda: |-
            id(total_energy).publish_state(0);

See Also
--------

- :doc:`power_meter`
- :doc:`/esphomeyaml/components/sensor/cse7766`
- :doc:`/esphomeyaml/components/sensor/hlw8012`
- :doc:`/esphomeyaml/components/sensor/pulse_counter`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/cookbook/total_energy.rst>`__

.. disqus::
