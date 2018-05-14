ESP32 Touch Pad Binary Sensor
=============================

The ``esp32_touch`` binary sensor platform lets you use the touch peripheral of the
ESP32 to detect if a certain pin is being "touched".

First, you need to setup the `global touch hub </esphomeyaml/components/esp32_touch.html>`__. Then
you can add individual touch pads as binary sensors. When a touch is detected on these pins, the binary
sensor will report an ``ON`` state. And, of course, if no touch is detected, the binary sensor will report
an ``OFF`` state.

|image0|

.. code:: yaml

    # Example configuration entry
    esp32_touch:

    binary_sensor:
      - platform: esp32_touch
        name: "ESP32 Touch Pad GPIO27"
        pin: GPIO27
        threshold: 1000

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

-  **pin** (**Required**, `pin </esphomeyaml/configuration-types.html#pin>`__): The pin to detect touch
   events on.
-  **threshold** (**Required**, int): The threshold to use to detect touch events. Smaller values mean
   a higher probability that the pad is being touched.
-  **name** (**Required**, string): The name of the binary sensor.
-  **id** (*Optional*,
   `id </esphomeyaml/configuration-types.html#id>`__): Manually specify
   the ID used for code generation.
-  All other options from `Binary
   Sensor </esphomeyaml/components/binary_sensor/index.html#base-binary-sensor-configuration>`__
   and `MQTT
   Component </esphomeyaml/components/mqtt.html#mqtt-component-base-configuration>`__.

Touch Pad Pins
~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~

For each touch pad you want to monitor, you need to find a threshold first. This threshold is
used to determine if a pad is being touched or not using the raw values from the sensor. Lower
raw values mean that it is more likely that a touch is happening. For example, values around
1000 to 1600 usually mean the pad is not being touched, and values in the range of 600 and less
mean the pad is probably being touched.

To find suitable threshold values, first configure the `ESP32 touch hub </esphomeyaml/components/esp32_touch.html>`__
to output measured values using the ``setup_mode:`` configuration option. Next, add some binary sensors
for the touch pads you want to observe. Also put some threshold in the configuration as seen below
to make the validator happy, we are going to find good thresholds in a moment anyway.

.. code:: yaml

    # Example configuration entry for finding threshold values
    esp32_touch:
      setup_mode: True

    binary_sensor:
      - platform: esp32_touch
        name: "ESP32 Touch Pad GPIO27"
        pin: GPIO27
        threshold: 1000

Then upload the program and open the logs, you will see values like these. Try touching the pins
and you will (hopefully) see the value decreasing a bit. Play around with different amounts of
force you put on the touch pad until you find a good value that can differentiate between
touch/non-touch events.

|image1|

Finally, put your threshold parameter in the configuration. Do not forget to disable the ``setup_mode``
option again by setting it to ``False``. Otherwise you will end up spamming the logs and slowing the device
down.

.. |image0| image:: /esphomeyaml/components/binary_sensor/esp32_touch.png
    :class: align-center
    :width: 80.0%

.. |image1| image:: /esphomeyaml/components/binary_sensor/esp32_touch_finding_thresholds.png
    :class: align-center
