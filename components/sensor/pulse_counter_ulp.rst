Pulse Counter ULP Sensor
========================

.. seo::
    :description: Instructions for setting up pulse counter ULP sensors.
    :image: pulse.svg

The pulse counter ULP sensor allows you to count the frequency of a pulse on a pin.

This sensor uses the ESP32's Ultra-Low Power (ULP) processor, which remains
active even in :doc:`deep sleep </components/deep_sleep>`. Only one ULP
component can run at a time.

This sensor is only available on the ESP32 using the IDF framework.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_counter_ulp
        pin: GPIOXX
        name: "Pulse Counter ULP"

Configuration variables
-----------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to count pulses on. This must be a valid RTC_GPIO pin.
- **count_mode** (*Optional*): Configure how the counter should behave
  on a detected rising edge/falling edge.

  - **rising_edge** (*Optional*): What to do when a rising edge is
    detected. One of ``DISABLE``, ``INCREMENT`` and ``DECREMENT``.
    Defaults to ``INCREMENT``.
  - **falling_edge** (*Optional*): What to do when a falling edge is
    detected. One of ``DISABLE``, ``INCREMENT`` and ``DECREMENT``.
    Defaults to ``DISABLE``.

- **sleep_duration** (*Optional*, :ref:`config-time`): How long the ULP program
  will sleep for between reads. Higher values will reduce battery consumption at
  the cost of missing shorter pulses. The shortest pulse that can be measured has
  a width of ``sleep_duration * (debounce + 1)``. Defaults to ``20ms``.
- **debounce** (*Optional*, int): Number of consecutive high or low inputs the
  ULP program needs to see to change state. Higher values will reduce the chance
  for false positives at the cost of missing shorter pulses. The shortest pulse
  that can be measured has a width of ``sleep_duration * (debounce + 1)``.
  Defaults to ``3``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check
  the sensor while awake. The sensor will not update while in deep sleep, but will
  update on wake regardless of ``update_interval``. Defaults to ``60s``.
- All other options from :ref:`Sensor <config-sensor>`.

.. note::

    See :doc:`integration sensor </components/sensor/integration>` for summing up pulse counter ULP
    values over time.

Converting units
----------------

The sensor defaults to measuring its values using a unit of measurement
of “pulses/min”. You can change this by using :ref:`sensor-filters`.
For example, if you're using the pulse counter with a photodiode to
count the light pulses on a power meter, you can do the following:

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_counter_ulp
        pin: GPIOXX
        unit_of_measurement: 'kW'
        name: 'Power Meter House'
        filters:
          - multiply: 0.06  # (60s/1000 pulses per kWh)

Wiring
------

If you want to count pulses from a simple reed switch, the simplest way is to make
use of the internal pull-up/pull-down resistors.

You can wire the switch between a GPIO pin and GND; in this case set the pin to input, pullup and inverted:

.. code-block:: yaml

    # Reed switch between GPIO and GND
    sensor:
      - platform: pulse_counter_ulp
        pin:
          number: 12
          inverted: true
          mode:
            input: true
            pullup: true
        name: "Pulse Counter ULP"

If you wire it between a GPIO pin and +3.3V, set the pin to input, pulldown:

.. code-block:: yaml

    # Reed switch between GPIO and +3.3V
    sensor:
      - platform: pulse_counter_ulp
        pin:
          number: 12
          mode:
            input: true
            pulldown: true
        name: "Pulse Counter ULP"

The safest way is to use GPIO + GND, as this avoids the possibility of short
circuiting the wire by mistake.

See Also
--------

- :ref:`sensor-filters`
- :doc:`/components/sensor/pulse_counter`
- :doc:`/components/sensor/pulse_meter`
- :doc:`rotary_encoder`
- `esp-idf GPIO table <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html>`__.
- `esp-idf Pulse Counter API <https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/ulp.html>`__.
- :apiref:`pulse_counter_ulp/pulse_counter_ulp_sensor.h`
- :ghedit:`Edit`
