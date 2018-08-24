ESP32 Touch Pad Hub
===================

The ``esp32_touch`` component creates a global hub for detecting touches on
the eight touch pads of the ESP32 as :doc:`binary senors </esphomeyaml/components/binary_sensor/esp32_touch>`.

.. code:: yaml

    # Example configuration entry
    esp32_touch:
      setup_mode: False

    binary_sensor:
      - platform: esp32_touch
        name: "ESP32 Touch Pad GPIO27"
        pin: GPIO27
        threshold: 1000

Configuration variables:
------------------------

-  **setup_mode** (*Optional*, boolean): Whether debug messages with the touch pad value should
   be displayed in the logs. Useful for finding out suitable thresholds for the binary sensors, but
   spam the logs. See :doc:`setting up touch pads </esphomeyaml/components/binary_sensor/esp32_touch>`
   for more information. Defaults to false.
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID for code generation.

Advanced options (the defaults are usually quite good, but if you're having accuracy issues, use these):

- **iir_filter** (*Optional*, :ref:`config-time`): Optionally set up an
  `Infinite Impulse Response <https://en.wikipedia.org/wiki/Infinite_impulse_response>`__
  filter should be applied to all touch pads. This can increase the accuracy of the touch pads a lot, but
  higher values decrease the response time. A good value to start with is ``10ms``. Default is no IIR filter.
- **sleep_duration** (*Optional*, :ref:`config-time`): Set a time period
  denoting the amount of time the touch peripheral should sleep between measurements. This can decrease
  power usage but make the sensor slower. Default is about 27 milliseconds.
- **measurement_duration** (*Optional*, :ref:`config-time`): Set the conversion
  time for all touch pads. A longer conversion time means that more charge/discharge cycles of the touch pad
  can be performed, therefore increasing accuracy. Default is about 8ms, the maximum amount.
- **low_voltage_reference** (*Optional*): The low voltage reference to use for the charge cycles. See
  the `esp-idf docs <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/touch_pad.html#optimization-of-measurements>`__
  for a nice explanation of this. One of ``0.5V``, ``0.6V``, ``0.7V``, ``0.8V``. Default is ``0.5V``.
- **high_voltage_reference** (*Optional*): The high voltage reference to use for the charge cycles. See
  the `esp-idf docs <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/touch_pad.html#optimization-of-measurements>`__
  for a nice explanation of this. One of ``2.4V``, ``2.5V``, ``2.6V``, ``2.7V``. Default is ``2.7V``.
- **voltage_attenuation** (*Optional*): The voltage attenuation to use for the charge cycles. See
  the `esp-idf docs <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/touch_pad.html#optimization-of-measurements>`__
  for a nice explanation of this. One of ``1.5V``, ``1V``, ``0.5V``, ``0V``. Default is ``0V``.

See Also
--------

- :doc:`binary_sensor/esp32_touch`
- :doc:`API Reference </api/binary_sensor/esp32_touch>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/esp32_touch.rst>`__
