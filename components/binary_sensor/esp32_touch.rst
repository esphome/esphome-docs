ESP32 Touch Pad
===============

.. seo::
    :description: Instructions for setting up the touch pad on the ESP32.
    :image: touch.svg

.. _esp32-touch-component:

Component/Hub
-------------

The ``esp32_touch`` component creates a global hub for detecting touches on
the eight touch pads of the ESP32 as :ref:`binary sensors <esp32-touch-binary-sensor>`.

.. code-block:: yaml

    # Example configuration entry
    esp32_touch:
      setup_mode: false

    binary_sensor:
      - platform: esp32_touch
        name: "ESP32 Touch Pad GPIO27"
        pin: GPIO27
        threshold: 1000

Configuration variables:
************************

-  **setup_mode** (*Optional*, boolean): Whether debug messages with the touch pad value should
   be displayed in the logs. Useful for finding out suitable thresholds for the binary sensors, but
   spam the logs. See :ref:`setting up touch pads <esp32-touch-binary-sensor>`
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
  the `esp-idf docs <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/touch_pad.html#optimization-of-measurements>`__
  for a nice explanation of this. One of ``0.5V``, ``0.6V``, ``0.7V``, ``0.8V``. Default is ``0.5V``.
- **high_voltage_reference** (*Optional*): The high voltage reference to use for the charge cycles. See
  the `esp-idf docs <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/touch_pad.html#optimization-of-measurements>`__
  for a nice explanation of this. One of ``2.4V``, ``2.5V``, ``2.6V``, ``2.7V``. Default is ``2.7V``.
- **voltage_attenuation** (*Optional*): The voltage attenuation to use for the charge cycles. See
  the `esp-idf docs <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/touch_pad.html#optimization-of-measurements>`__
  for a nice explanation of this. One of ``1.5V``, ``1V``, ``0.5V``, ``0V``. Default is ``0V``.

.. _esp32-touch-binary-sensor:

Binary Sensor
-------------

The ``esp32_touch`` binary sensor platform lets you use the touch peripheral of the
ESP32 to detect if a certain pin is being "touched".

First, you need to setup the :ref:`global touch hub <esp32-touch-component>`. Then
you can add individual touch pads as binary sensors. When a touch is detected on these pins, the binary
sensor will report an ``ON`` state. And, of course, if no touch is detected, the binary sensor will report
an ``OFF`` state.

.. figure:: images/esp32_touch-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    esp32_touch:

    binary_sensor:
      - platform: esp32_touch
        name: "ESP32 Touch Pad GPIO27"
        pin: GPIO27
        threshold: 1000

Configuration variables:
************************

-  **pin** (**Required**, :ref:`config-pin`): The pin to detect touch
   events on.
-  **threshold** (**Required**, int): The threshold to use to detect touch events. Smaller values mean
   a higher probability that the pad is being touched.
-  **name** (**Required**, string): The name of the binary sensor.
-  **id** (*Optional*,
   :ref:`config-id`): Manually specify
   the ID used for code generation.
-  **wakeup_threshold** (*Optional*, int): The threshold to use to detect touch events to wakeup from deep
   sleep. Smaller values mean a higher probability that the pad is being touched. All touch pad sensors that
   should trigger a wakeup from deep sleep must specify this value. The :ref:`deep_sleep-component` must also
   be configured to enable a wakeup from a touch event. Note that no filter is active during deep sleep.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`.

Touch Pad Pins
--------------

8 pins on the ESP32 can be used to detect touches. These are (in the default "raw" pin names):

-  ``GPIO0``
-  ``GPIO2``
-  ``GPIO4``
-  ``GPIO12``
-  ``GPIO13``
-  ``GPIO14``
-  ``GPIO15``
-  ``GPIO27``
-  ``GPIO32``
-  ``GPIO33``

Finding thresholds
------------------

For each touch pad you want to monitor, you need to find a threshold first. This threshold is
used to determine if a pad is being touched or not using the raw values from the sensor. Lower
raw values mean that it is more likely that a touch is happening. For example, values around
1000 to 1600 usually mean the pad is not being touched, and values in the range of 600 and less
mean the pad is probably being touched.

To find suitable threshold values, first configure the :ref:`ESP32 touch hub <esp32-touch-component>`
to output measured values using the ``setup_mode:`` configuration option. Next, add some binary sensors
for the touch pads you want to observe. Also put some threshold in the configuration as seen below
to make the validator happy, we are going to find good thresholds in a moment anyway.

.. code-block:: yaml

    # Example configuration entry for finding threshold values
    esp32_touch:
      setup_mode: true

    binary_sensor:
      - platform: esp32_touch
        name: "ESP32 Touch Pad GPIO27"
        pin: GPIO27
        threshold: 1000

Then upload the program and open the logs, you will see values like these. Try touching the pins
and you will (hopefully) see the value decreasing a bit. Play around with different amounts of
force you put on the touch pad until you find a good value that can differentiate between
touch/non-touch events.

.. figure:: images/esp32_touch-finding_thresholds.png
    :align: center

Finally, put your threshold parameter in the configuration. Do not forget to disable the ``setup_mode``
option again by setting it to ``false``. Otherwise you will end up spamming the logs and slowing the device
down.

See Also
--------

- :doc:`/components/binary_sensor/index`
- :apiref:`esp32_touch/esp32_touch.h`
- `esp-idf Touch Sensor API <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/touch_pad.html>`__
- :ghedit:`Edit`
